from DBcontext import DBContext
import asyncio


postgresConfigs = {
    "host": "localhost",
    "port": 5432,
    "username": "postgres",
    "password": "postgres",
    "databases": [
        {
            "name": "test_db",
        }
    ]
}

db_context = DBContext()

# Get PostgreSQL schema using the DBContext

schema = asyncio.run(db_context.get_postgreSQL_schema(
    host=postgresConfigs["host"],
    port=postgresConfigs["port"],
    username=postgresConfigs["username"],
    password=postgresConfigs["password"],
    databases=postgresConfigs["databases"]
))

# Print the schema (optional, for verification)
print("PostgreSQL Schema:")
print(schema)
