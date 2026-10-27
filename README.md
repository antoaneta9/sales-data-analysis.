# Sales Data Analysis with Python, Pandas & SQL

## Overview

This project explores a sales dataset using Python, Pandas, and SQL. It demonstrates the fundamentals of data cleaning, data transformation, relational databases, and business-oriented data analysis.

The project uses sample order and customer data to calculate sales metrics and explore purchasing patterns across products, categories, and cities.

## Technologies

- **Python** — data processing and pipeline execution
- **Pandas** — data loading, cleaning, validation, and transformation
- **SQL** — querying, aggregation, joins, and analysis
- **SQLite** — storing structured data in a relational database
- **Logging** — tracking pipeline execution and errors

## Project Structure

```text
data_engineering_beginner_project/
├── data/
│   ├── orders.csv
│   └── customers.csv
├── main.py
├── load_customers.py
├── analysis.sql
├── requirements.txt
├── .gitignore
└── README.md
```

## What the Project Does

### 1. Data Loading
- Reads order data from a CSV file using Pandas.
- Parses order dates and checks data types.

### 2. Data Quality and Cleaning
- Checks for missing values and duplicate records.
- Validates quantities and prices.
- Removes duplicate rows and records with missing required values.
- Filters out invalid quantities and prices.

### 3. Data Transformation
- Calculates `total_amount` for each order using quantity and price.
- Prepares the cleaned data for storage and analysis.

### 4. Database Loading
- Loads sales data into a SQLite database.
- Uses a staging table and incremental loading to avoid inserting existing order IDs again.
- Loads customer data into a separate table.

### 5. SQL Analysis
The SQL queries explore:
- Top products by total sales.
- Sales totals by category.
- Relationships between orders and customers using `JOIN`.
- Orders without matching customer records using `LEFT JOIN`.
- Total sales by city.

### 6. Logging
The pipeline records execution events and errors in a log file.

## How to Run

### Prerequisites
- Python 3.10 or newer recommended
- pip

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the sales pipeline

```bash
python main.py
```

### 3. Load customer data

```bash
python load_customers.py
```

### 4. Run the SQL analysis

Open `analysis.sql` in a SQLite-compatible SQL editor and execute the queries against `sales.db`.

## Key Learning Outcomes

Through this project, I practised:

- Working with CSV data using Pandas.
- Performing data quality checks and cleaning.
- Creating calculated columns and transforming data.
- Loading data into a relational database.
- Writing SQL queries with aggregations and joins.
- Implementing basic incremental loading.
- Using logging to track execution and errors.

## Project Purpose

This project was created as part of my practical learning journey in Python, Pandas, and SQL, with a focus on building a foundation for further study in data analysis and data engineering.
