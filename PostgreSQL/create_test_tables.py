import asyncpg
import asyncio
import os
import csv

async def connect_to_db(username, password, dbname, host, port):
    try:
        conn = await asyncpg.connect(
                user=username,
                password=password,
                database=dbname,
                host=host,
                port=port
            )
        print("Connected to the database successfully.")
        return conn
    except Exception as e:
        print(f"Unable to connect to the database: {e}")
        return None

async def execute_sql_file(conn, file_path):
    try:
        with open(file_path, 'r') as file:
            sql_commands = file.read()

        await conn.execute(sql_commands)
        print(f"SQL commands from {file_path} executed successfully.")
    except asyncpg.PostgresError as e:
        print(f"Error executing SQL commands from {file_path}: {e}")
    except IOError as e:
        print(f"Error reading SQL file {file_path}: {e}")

async def create_table_from_csv(conn, csv_file_path):
    table_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    
    with open(csv_file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        headers = next(csv_reader)
        
        # Create a simple table structure
        columns = [f"{header.lower().replace(' ', '_')} TEXT" for header in headers]
        create_table_sql = f"""
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} (
            {', '.join(columns)}
        );
        """
        
        await conn.execute(create_table_sql)
        print(f"Table {table_name} created successfully.")

async def upload_files_to_postgres(username, password, dbname, host, port, csv_directory):
    conn = await connect_to_db(username, password, dbname, host, port)
    if conn:
        try:
            for filename in os.listdir(csv_directory):
                if filename.endswith('.csv'):
                    file_path = os.path.join(csv_directory, filename)
                    await create_table_from_csv(conn, file_path)
        finally:
            await conn.close()
            print("Database connection closed.")

def create_test_tables(username, password, dbname, host, port, csv_directory):
    asyncio.run(upload_files_to_postgres(username, password, dbname, host, port, csv_directory))

# Example usage:
# create_test_tables('your_username', 'your_password', 'your_database', 'localhost', 5432, 'test_data/random_header_test')
