import asyncio
import asyncpg
from Embedding.embeddings import TransformerEmbeddingModel, evaluate_column_descriptors, process_csv_embeddings, compare_embeddings, embed_table_columns, embed_table_descriptions

model = TransformerEmbeddingModel()


def test_embedding_csv():
    col_embs = process_csv_embeddings('names.csv', model)
    description_embs = {"Name": model.get_embeddings(["First name of student."])}
    print(col_embs)
    lowest_indices, sim_matrix = compare_embeddings(col_embs, description_embs)
    print(lowest_indices, sim_matrix)
    print("TransformerEmbeddingModel test passed")


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

async def test_embedding_postgres():
    conn = await asyncpg.connect(user=postgresConfigs["username"], password=postgresConfigs["password"], database=postgresConfigs["databases"][0]["name"], host=postgresConfigs["host"], port=postgresConfigs["port"])
    columns_to_check = await evaluate_column_descriptors("product_sales", conn, model)
    print(columns_to_check)

if __name__ == "__main__":
    asyncio.run(test_embedding_postgres())
