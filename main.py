import asyncpg
from DBcontext import DBContext
import asyncio
from CodeExecution.CreateDocker import load_docker as create_docker
from CodeExecution.ScriptExecution import run_command, write_file, execute_script, create_and_execute_file
from Embedding.embeddings import TransformerEmbeddingModel, evaluate_column_descriptors
from Configs.AzureOpenAIConfig import asyncAzureOpenAIClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

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
client = asyncAzureOpenAIClient

db_context = DBContext()

# Register PostgreSQL configurations
db_context.register_postgres_configs(postgresConfigs)

async def main():
    # Boot a docker container at the start of main


    # Get PostgreSQL schema using the DBContext
    Goodschema = await db_context.get_postgreSQL_schema_Better(
        host=postgresConfigs["host"],
        port=postgresConfigs["port"],
        username=postgresConfigs["username"],
        password=postgresConfigs["password"],
        databases=postgresConfigs["databases"]
    )


    # Print the schema (optional, for verification)



    
    

  

# Run the async main function
asyncio.run(main())
