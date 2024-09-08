import asyncpg
import asyncio
import os
import csv

async def create_test_tables(username, password, dbname, host, port, csv_directory):
    try:
        # Connect to the database
        conn = await asyncpg.connect(user=username, password=password, database=dbname, host=host, port=port)

        # Get all CSV files in the directory
        csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

        for csv_file in csv_files:
            table_name = os.path.splitext(csv_file)[0]
            file_path = os.path.join(csv_directory, csv_file)

            # Read CSV file
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                headers = next(reader)
                
                # Create table (drop if exists)
                columns = ', '.join([f'"{header}" TEXT' for header in headers])
                await conn.execute(f'DROP TABLE IF EXISTS "{table_name}"')
                await conn.execute(f'CREATE TABLE "{table_name}" ({columns})')

                # Insert data
                for row in reader:
                    placeholders = ','.join(['$' + str(i) for i in range(1, len(row) + 1)])
                    await conn.execute(f'INSERT INTO "{table_name}" VALUES ({placeholders})', *row)

        print(f"All tables created successfully in database {dbname}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        if conn:
            await conn.close()

# Example usage:
# asyncio.run(create_test_tables('your_username', 'your_password', 'your_database', 'localhost', 5432, 'test_data/random_header_test'))
