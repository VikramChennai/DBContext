import argparse
import asyncpg
import asyncio


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
        print("SQL commands executed successfully.")
    except asyncpg.PostgresError as e:
        print(f"Error executing SQL commands: {e}")
    except IOError as e:
        print(f"Error reading SQL file: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Set up database tables and import data.")
    parser.add_argument("--username", required=True, help="Database username")
    parser.add_argument("--password", required=True, help="Database password")
    parser.add_argument("--database", required=True, help="Database name")
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--port", required=True, help="Database port")
    parser.add_argument("--sql_file", required=True, help="Path to SQL file")

    args = parser.parse_args()

    conn = await connect_to_db(args.username, args.password, args.database, args.host, args.port)
    if conn:
        await execute_sql_file(conn, args.sql_file)
        await conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    asyncio.run(main())
