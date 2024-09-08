import asyncpg
import random
from Configs.AnthropicConfig import AnthropicClient
from Configs.AzureOpenAIConfig import asyncAzureOpenAIClient, deployment_name

async def get_postgreSQL_schema_Better(host: str, port: int, username: str, password: str, databases: list) -> list:
    updated_databases = []

    for db in databases:
        dbname = db['name']
        schema = {}

        try:
            connection = await asyncpg.connect(
                user=username,
                password=password,
                database=dbname,
                host=host,
                port=port
            )

            # Query to get tables
            tables_query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            """
            tables = await connection.fetch(tables_query)

            # Fetch columns for each table
            for table in tables:
                table_name = table['table_name']
                schema[table_name] = {}

                # Query to get columns for the table
                columns_query = f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = '{table_name}'
                """
                columns = await connection.fetch(columns_query)

                schema[table_name]['columns'] = {
                    col['column_name']: {
                        'data_type': col['data_type'],
                        'is_nullable': col['is_nullable']
                    }
                    for col in columns
                }

                # Print out the table name
                print(f"\nTable: {table_name}")
                print("=" * (len(table_name) + 7))

                # Print column headers
                print(f"{'Column Name':<20} {'Data Type':<15} {'Nullable':<10} {'Description':<50}")
                print("-" * 95)

                for col in columns:
                    column_name = col['column_name']
                    values_query = f"""
                    SELECT "{column_name}" FROM "{table_name}"
                    """
                    values = await connection.fetch(values_query)
                    sample_values = random.sample(values, min(10, len(values)))

                    # Generate column description using Azure OpenAI
                    prompt = f"Describe the column '{column_name}' in the table '{table_name}' based on these sample values: {[v[column_name] for v in sample_values]}. Consider the column name, data type, and nullability. Also make sure to make your description as concise as possible. You are penalized for long rambling descriptions"
                    
                    response = await asyncAzureOpenAIClient.chat.completions.create(
                        model=deployment_name,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant that describes database columns based on their name, data type, and sample values."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    column_description = response.choices[0].message.content.strip()
                    schema[table_name]['columns'][column_name]['description'] = column_description

                    # Print column information
                    print(f"{column_name:<20} {col['data_type']:<15} {col['is_nullable']:<10} {column_description[:50]:<50}")

                # Query to get primary keys for the table
                primary_keys_query = f"""
                SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_schema = 'public' AND tc.table_name = '{table_name}' AND tc.constraint_type = 'PRIMARY KEY'
                """
                primary_keys = await connection.fetch(primary_keys_query)

                schema[table_name]['primary_keys'] = [pk['column_name'] for pk in primary_keys]

            await connection.close()
        except Exception as e:
            schema = {"error": str(e)}

        updated_db = db.copy()
        updated_db['schema'] = schema
        updated_databases.append(updated_db)

    return updated_databases[0]

async def get_postgreSQL_schema_Bad(host: str, port: int, username: str, password: str, databases: list) -> list:
    updated_databases = []

    for db in databases:
        dbname = db['name']
        schema = {}

        try:
            connection = await asyncpg.connect(
                user=username,
                password=password,
                database=dbname,
                host=host,
                port=port
            )

            # Query to get tables
            tables_query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            """
            tables = await connection.fetch(tables_query)

            # Fetch columns for each table
            for table in tables:
                table_name = table['table_name']
                schema[table_name] = {}

                # Query to get columns for the table
                columns_query = f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = '{table_name}'
                """
                columns = await connection.fetch(columns_query)

                schema[table_name]['columns'] = {
                    col['column_name']: {
                        'data_type': col['data_type'],
                        'is_nullable': col['is_nullable']
                    }
                    for col in columns
                }

                # Query to get primary keys for the table
                primary_keys_query = f"""
                SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                WHERE tc.table_schema = 'public' AND tc.table_name = '{table_name}' AND tc.constraint_type = 'PRIMARY KEY'
                """
                primary_keys = await connection.fetch(primary_keys_query)

                schema[table_name]['primary_keys'] = [pk['column_name'] for pk in primary_keys]

            await connection.close()
        except Exception as e:
            schema = {"error": str(e)}

        updated_db = db.copy()
        updated_db['schema'] = schema
        updated_databases.append(updated_db)

    return updated_databases[0]