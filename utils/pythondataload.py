import pandas as pd
import psycopg2
import psycopg2.extras

def clean_text(text):
    """
    Clean text data by removing leading/trailing whitespaces and converting to string.
    """
    if pd.isna(text):
        return None
    return str(text).strip()

def convert_numeric(val):
    """
    Convert value to float if possible, otherwise return None.
    """
    try:
        return float(val) if pd.notna(val) else None
    except (ValueError, TypeError):
        return None

def load_data_to_postgres(merged_file, dbname, user, password, host="localhost", port="5432", batch_size=10000):
    """
    Load data from a CSV file into a PostgreSQL table with error handling and upsert functionality.

    Args:
        merged_file (str): Path to the CSV file containing college data.
        dbname (str): Name of the PostgreSQL database.
        user (str): Username for database access.
        password (str): Password for database access.
        host (str, optional): Hostname of the PostgreSQL server (default: "localhost").
        port (str, optional): Port number of the PostgreSQL server (default: "5432").
        batch_size (int, optional): Number of rows to insert per batch (default: 10000).
    """

    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # Read CSV data using low_memory for large datasets
        merged_df = pd.read_csv(merged_file, encoding='latin1', low_memory=False)

        # Prepare column list for INSERT query
        column_list = ', '.join(merged_df.columns.tolist())

        # Define upsert query with EXCLUDE clause for conflict handling
        upsert_query = f"""
            INSERT INTO colleges ({column_list})
            VALUES %s
            ON CONFLICT (unitid) DO UPDATE SET
                {column_list[1:]} = EXCLUDED.{column_list[1:]}
        """

        # Use psycopg2.extras.execute_values for efficient batch inserts
        data_tuples = [tuple(row) for _, row in merged_df.iterrows()]
        psycopg2.extras.execute_values(cur, upsert_query, data_tuples, batch=batch_size)

        conn.commit()
        print("Data loaded successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Error while loading data:", error)
        conn.rollback()  # Rollback on error

    finally:
        if conn:
            cur.close()
            conn.close()

# Example usage
merged_file = "your_merged_data.csv" 
# Replace with your database credentials
dbname = "your_database_name" 
user = "your_username" 
password = "your_password" 

load_data_to_postgres(merged_file, dbname, user, password)