import asyncpg

async def get_postgreSQL_schema(host: str, port: int, username: str, password: str, databases: list) -> list:
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
            #(f"Connection to {dbname} failed: {str(e)}")
            schema = {"error": str(e)}

        updated_db = db.copy()
        updated_db['schema'] = schema
        updated_databases.append(updated_db)

    return updated_databases