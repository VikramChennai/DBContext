from PostgreSQL.postgreSQL import get_postgreSQL_schema

class DBContext:
    def __init__(self):
        self.Embedding_Model = None
        self.cursor = None
        self.database_name = None

    async def get_postgreSQL_schema(self, host: str, port: int, username: str, password: str, databases: list) -> str:
        self.postgreSQL_schema = await get_postgreSQL_schema(host, port, username, password, databases)
        return self.postgreSQL_schema



