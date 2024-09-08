from DBcontext import DBContext
import asyncio


postgresConfigs = {
    "host": "localhost",
    "port": 5432,
    "username": "postgres",
    "password": "new!Phase1",
    "databases": [
        {
            "name": "test_db",
        }
    ]
}

db_context = DBContext()

# Register PostgreSQL configurations
db_context.register_postgres_configs(postgresConfigs)

async def main():
    # Get PostgreSQL schema using the DBContext
    schema = await db_context.get_postgreSQL_schema(
        host=postgresConfigs["host"],
        port=postgresConfigs["port"],
        username=postgresConfigs["username"],
        password=postgresConfigs["password"],
        databases=postgresConfigs["databases"]
    )

    # Print the schema (optional, for verification)
    print("PostgreSQL Schema:")
    print(schema)
    # Call create_test_tables with the correct parameters
    await db_context.create_test_tables(
        host=postgresConfigs["host"],
        port=postgresConfigs["port"],
        username=postgresConfigs["username"],
        password=postgresConfigs["password"],
        databases=postgresConfigs["databases"][0]["name"],
        csv_directory='test_data/random_header_test'
    )

# Run the async main function
asyncio.run(main())
