from DBcontext import DBContext
import asyncio
from CodeExecution.CreateDocker import load_docker as create_docker
from CodeExecution.ScriptExecution import run_command, write_file, execute_script, create_and_execute_file

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
    # Boot a docker container at the start of main
    container = create_docker()

    try:
        # Get PostgreSQL schema using the DBContext
        schema = await db_context.get_postgreSQL_schema_Better(
            host=postgresConfigs["host"],
            port=postgresConfigs["port"],
            username=postgresConfigs["username"],
            password=postgresConfigs["password"],
            databases=postgresConfigs["databases"]
        )

        # Print the schema (optional, for verification)
        print("PostgreSQL Schema:")
        print(schema)




        # Create a Python file that prints "Hello World" in the container
        container.exec_run("sh -c 'echo \"print(\\\"Hello World\\\")\" > hello_world.py'")

        # Run the Python file
        result = container.exec_run("python hello_world.py")

        # Get the output
        output = result.output.decode('utf-8').strip()

        # Validate that "Hello World" was printed
        assert output == "Hello World", f"Expected 'Hello World', but got '{output}'"

        print("Hello World test passed successfully!")

    finally:
        # Stop and remove the container
        container.stop()
        container.remove()

# Run the async main function
asyncio.run(main())
