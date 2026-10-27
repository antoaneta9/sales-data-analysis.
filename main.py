import logging
import sqlite3
from pathlib import Path
import pandas as pd


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "orders.csv"
DB_PATH = BASE_DIR / "sales.db"
LOG_PATH = BASE_DIR / "pipeline.log"

logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

def main():
    connection = None

    try:
        # 1. EXTRACT: Read the source CSV file
        logger.info("Pipeline started")

        df = pd.read_csv(
            DATA_PATH,
            parse_dates=["order_date"],
        )

        logger.info("Read %s rows from CSV", len(df))

        # 2. VALIDATE: Check the source data
        required_columns = [
            "order_id",
            "customer_id",
            "order_date",
            "product",
            "category",
            "quantity",
            "price",
        ]

        missing_columns = set(required_columns) - set(df.columns)

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {sorted(missing_columns)}"
            )

        if df["order_id"].isna().any():
            raise ValueError("order_id contains missing values")

        if df["order_id"].duplicated().any():
            raise ValueError("Duplicate order_id values found")

        if df["order_id"].isna().any():
            raise ValueError("order_id contains missing values")

        logger.info("Source data validation completed")

        # 3. TRANSFORM: Clean the data
        rows_before = len(df)

        df = df.drop_duplicates()

        df = df.dropna(
            subset=[
                "order_id",
                "customer_id",
                "order_date",
                "product",
                "category",
                "quantity",
                "price",
            ]
        ).copy()

        df = df[
            (df["quantity"] > 0)
            & (df["price"] >= 0)
        ].copy()

        df["category"] = df["category"].astype("category")

        df["total_amount"] = df["quantity"] * df["price"]

        logger.info(
            "Transformation completed: %s rows before cleaning, %s after",
            rows_before,
            len(df),
        )

        # 4. LOAD: Connect to SQLite
        connection = sqlite3.connect(DB_PATH)

        # Create the target table with a primary key
        connection.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                product TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                total_amount REAL NOT NULL
            )
        """)

        # Prepare data for SQL loading
        df_to_load = df.copy()
        df_to_load["category"] = df_to_load["category"].astype("string")
        df_to_load["order_date"] = (
            df_to_load["order_date"].dt.strftime("%Y-%m-%d")
        )

        # Load into a staging table
        df_to_load.to_sql(
            "sales_staging",
            connection,
            if_exists="replace",
            index=False,
        )

        # Insert only records that do not already exist
        connection.execute("""
            INSERT INTO sales (
                order_id,
                customer_id,
                order_date,
                product,
                category,
                quantity,
                price,
                total_amount
            )
            SELECT
                st.order_id,
                st.customer_id,
                st.order_date,
                st.product,
                st.category,
                st.quantity,
                st.price,
                st.total_amount
            FROM sales_staging AS st
            WHERE NOT EXISTS (
                SELECT 1
                FROM sales AS s
                WHERE s.order_id = st.order_id
            )
        """)

        connection.commit()

        logger.info("Data loading completed")

        # 5. ANALYZE: Run SQL queries
        category_query = """
            SELECT
                category,
                SUM(total_amount) AS total_sales
            FROM sales
            GROUP BY category
            ORDER BY total_sales DESC
        """

        category_results = pd.read_sql_query(
            category_query,
            connection,
        )

        print("\nSales by category:")
        print(category_results)

        count_query = "SELECT COUNT(*) AS total_rows FROM sales"

        row_count = pd.read_sql_query(
            count_query,
            connection,
        )

        print("\nTotal rows in SQL table:")
        print(row_count)

        logger.info("Pipeline completed successfully")

    except (ValueError, OSError, sqlite3.Error, pd.errors.DatabaseError):
        logger.exception("Pipeline failed")
        raise

    finally:
        if connection is not None:
            connection.close()
            logger.info("Database connection closed")


if __name__ == "__main__":
    main()
