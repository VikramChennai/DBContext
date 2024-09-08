from PostgreSQL.postgreSQL import get_postgreSQL_schema_Better
from PostgreSQL.create_test_tables import create_test_tables

class DBContext():
    def __init__(self):
        self.Embedding_Model = None
        self.postgresConfigs = None

    def register_postgres_configs(self, configs):
        self.postgresConfigs = configs

    async def get_postgreSQL_schema_Better(self, host: str, port: int, username: str, password: str, databases: list) -> str:
        self.postgreSQL_schema = await get_postgreSQL_schema_Better(host, port, username, password, databases)
        return self.postgreSQL_schema
    
    async def create_test_tables(self, host: str, port: int, username: str, password: str, databases: str, csv_directory: str) -> str:
        print(f"Creating test tables for {databases} on {host}:{port} with user {username}")
        print(f"Password: {password}")  # Added line to print password
        self.postgreSQL_schema = await create_test_tables(host=host, port=port, username=username, password=password, dbname=databases, csv_directory=csv_directory)
        return self.postgreSQL_schema



