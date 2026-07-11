# Python Script: Load Cleaned Dataset into MySQL Database
# Uses sqlalchemy and pymysql

import os
import pandas as pd
from sqlalchemy import create_engine, text

def load_data():
    # Database connection parameters (override via env variables if needed)
    host = os.getenv("DB_HOST", "127.0.0.1")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "real_estate")

    print(f"Database settings: Host={host}, User={user}, Port={port}, DB={db_name}")

    # Create connection URLs
    server_url = f"mysql+pymysql://{user}:{password}@{host}:{port}"
    db_url = f"{server_url}/{db_name}"

    try:
        # 1. Read CSV file
        csv_path = "data/cleaned_data.csv"
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Cleaned data file not found at {csv_path}. Please run data cleaning first.")
        
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} records from {csv_path}")

        # 2. Connect to MySQL server and ensure database exists
        server_engine = create_engine(server_url)
        with server_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
            conn.commit()
        print(f"Ensured database '{db_name}' exists.")

        # 3. Connect to target database and execute create_schema.sql to set up structure
        db_engine = create_engine(db_url)
        
        schema_path = "sql/create_schema.sql"
        if os.path.exists(schema_path):
            print(f"Reading schema file: {schema_path}...")
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            
            # Execute schema statements
            with db_engine.connect() as conn:
                # Basic parsing: split by semicolon
                statements = schema_sql.split(";")
                for stmt in statements:
                    stmt = stmt.strip()
                    if stmt and not stmt.startswith("--"):
                        conn.execute(text(stmt))
                        conn.commit()
            print("Schema execution finished successfully.")
        else:
            print("Warning: sql/create_schema.sql not found. Table structure will be created by pandas.")

        # 4. Insert data using pandas to_sql (append mode to preserve custom schema types)
        print("Inserting records into 'properties' table...")
        df.to_sql(name="properties", con=db_engine, if_exists="append", index=False)
        print("Data insertion completed.")

        # 5. Verify insertion
        with db_engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM properties"))
            count = result.scalar()
            print(f"Verification successful: {count} records found in database properties table.")

    except Exception as e:
        print(f"ERROR: Failed to load data to MySQL database: {e}")
        print("\nNote: Please make sure MySQL is running locally on the specified port and you have appropriate privileges.")

if __name__ == "__main__":
    load_data()
