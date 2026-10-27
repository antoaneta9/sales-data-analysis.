
import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

customers = pd.read_csv(
    BASE_DIR / "data" / "customers.csv"
)

connection = sqlite3.connect(BASE_DIR / "sales.db")

try:
    customers.to_sql(
        "customers",
        connection,
        if_exists="replace",
        index=False
    )
    print("Customers loaded successfully!")
finally:
    connection.close()
