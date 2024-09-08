import psycopg2
from psycopg2 import sql
import argparse

def connect_to_db(username, password, database, host, port):
    try:
        conn = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            host=host,
            port=port
        )
        print("Connected to the database successfully.")
        return conn
    except psycopg2.Error as e:
        print(f"Unable to connect to the database: {e}")
        return None

def execute_sql_file(conn, file_path):
    try:
        with open(file_path, 'r') as file:
            sql_commands = file.read()

        with conn.cursor() as cur:
            cur.execute(sql_commands)
        conn.commit()
        print("SQL commands executed successfully.")
    except psycopg2.Error as e:
        print(f"Error executing SQL commands: {e}")
        conn.rollback()
    except IOError as e:
        print(f"Error reading SQL file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Set up database tables and import data.")
    parser.add_argument("--username", required=True, help="Database username")
    parser.add_argument("--password", required=True, help="Database password")
    parser.add_argument("--database", required=True, help="Database name")
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--port", required=True, help="Database port")
    parser.add_argument("--sql_file", required=True, help="Path to SQL file")

    args = parser.parse_args()

    conn = connect_to_db(args.username, args.password, args.database, args.host, args.port)
    if conn:
        execute_sql_file(conn, args.sql_file)
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
