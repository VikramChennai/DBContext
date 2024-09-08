import torch
import pandas as pd

from abc import ABC, abstractmethod
import numpy as np

class EmbeddingModel(ABC):
    @abstractmethod
    def get_embeddings(self, texts):
        pass

class TransformerEmbeddingModel(EmbeddingModel):
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        from transformers import AutoTokenizer, AutoModel
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def get_embeddings(self, texts):
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt", max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)

class OpenAIEmbeddingModel(EmbeddingModel):
    def __init__(self, model_name="text-embedding-ada-002"):
        import openai
        self.model_name = model_name

    def get_embeddings(self, texts):
        import openai
        response = openai.Embedding.create(input=texts, model=self.model_name)
        return torch.tensor([item['embedding'] for item in response['data']])

def process_csv_embeddings(csv_filename, embedding_model):
    df = pd.read_csv(csv_filename, header=0)
    column_embeddings = {column: embedding_model.get_embeddings(df[column].astype(str).tolist()) for column in df.columns}
    return column_embeddings


def load_embeddings(file_path):
    return torch.load(file_path)

def calculate_similarity(col_embeddings, desc_embeddings):
    column_similarities = {}
    for column, col_embedding in col_embeddings.items():
        desc_embedding = desc_embeddings[column]
        # Reshape desc_embedding to (1, 384) for broadcasting
        desc_embedding = desc_embedding.view(1, -1)
        # Normalize the embeddings
        col_embedding_normalized = col_embedding / col_embedding.norm(dim=1, keepdim=True)
        desc_embedding_normalized = desc_embedding / desc_embedding.norm()
        # Calculate cosine similarity for this column
        similarity = torch.mm(col_embedding_normalized, desc_embedding_normalized.t())
        column_similarities[column] = similarity.squeeze()

    # Stack the column similarities
    return torch.stack(list(column_similarities.values())).squeeze()


def get_lowest_indices(similarities, top_n=5):
    return similarities.argsort(dim=0)[:top_n].T

def compare_embeddings(embeddings1, embeddings2, top_n=5):
    # Calculate cosine similarity
    similarities = calculate_similarity(embeddings1, embeddings2)
    # Get the indices of the lowest similarity scores
    lowest_sim_indices = get_lowest_indices(similarities, top_n)
    return lowest_sim_indices, similarities

def compare_embedding_files(stored_embeddings_file, descriptor_embeddings_file, top_n=5):
    # Load the column embeddings and the descriptor embeddings
    stored_embeddings = load_embeddings(stored_embeddings_file)
    descriptor_embeddings = load_embeddings(descriptor_embeddings_file)
    return compare_embeddings(stored_embeddings, descriptor_embeddings)

async def get_table_data(table_name, connection):
    """
    Read a table from a database given the table name and asyncpg connection.
    
    :param table_name: Name of the table to read
    :param connection: asyncpg connection object
    :return: pandas DataFrame containing the table data
    """
    query = f"SELECT * FROM {table_name}"
    records = await connection.fetch(query)
    return pd.DataFrame(records)

async def embed_table_columns(table_name, connection, embedding_model):
    """
    Read a table from a database and create embeddings for its columns.
    
    :param table_name: Name of the table to process
    :param connection: asyncpg connection object
    :param embedding_model: An instance of EmbeddingModel to use for creating embeddings
    :return: Dictionary of column embeddings
    """
    df = await get_table_data(table_name, connection)
    column_embeddings = {column: embedding_model.get_embeddings(df[column].astype(str).tolist()) for column in df.columns}
    return column_embeddings

async def embed_table_descriptions(table_name, connection, embedding_model):
    """
    Read a table's column descriptions from a database and create embeddings for them.
    
    :param table_name: Name of the table to process
    :param connection: asyncpg connection object
    :param embedding_model: An instance of EmbeddingModel to use for creating embeddings
    :return: Dictionary of column description embeddings
    """
    query = f"""
    SELECT column_name, col_description((table_schema || '.' || table_name)::regclass::oid, ordinal_position) as column_description
    FROM information_schema.columns
    WHERE table_name = $1
    """
    records = await connection.fetch(query, table_name)
    descriptions = {record['column_name']: record['column_description'] or '' for record in records}
    description_embeddings = {column: embedding_model.get_embeddings([desc]) for column, desc in descriptions.items()}
    return description_embeddings


async def evaluate_column_descriptors(table_name, connection, embedding_model):
    """
    Evaluate column descriptors by comparing them with the actual data in the columns.

    :param table_name: Name of the table to process
    :param connection: asyncpg connection object
    :param embedding_model: An instance of EmbeddingModel to use for creating embeddings
    :return: Dictionary with evaluation results for each column
    """
    # Get column data and descriptions
    column_data = await embed_table_columns(table_name, connection, embedding_model)
    column_descriptions = await embed_table_descriptions(table_name, connection, embedding_model)

    # Set threshold parameters
    similarity_threshold = 0.3  # Minimum cosine similarity
    percentage_threshold = 0.8  # Minimum percentage of rows that should meet the similarity threshold
    n_least_similar = 5  # Number of least similar rows to return if threshold is not met

    results = {}

    for column, data_embeddings in column_data.items():
        if column not in column_descriptions:
            results[column] = {"error": "No description found"}
            continue

        desc_embedding = column_descriptions[column]
        similarities = calculate_similarity(data_embeddings.unsqueeze(0), desc_embedding).squeeze()

        # Calculate the percentage of rows meeting the similarity threshold
        percentage_above_threshold = (similarities >= similarity_threshold).float().mean().item()

        if percentage_above_threshold >= percentage_threshold:
            results[column] = {
                "status": "Good",
                "percentage_above_threshold": percentage_above_threshold
            }
        else:
            # Get the indices of the n least similar rows
            least_similar_indices = get_lowest_indices(similarities, n_least_similar).squeeze()
            
            # Get the actual data for these rows
            df = await get_table_data(table_name, connection)
            least_similar_rows = df.iloc[least_similar_indices.tolist()][column].tolist()

            results[column] = {
                "status": "Needs improvement",
                "percentage_above_threshold": percentage_above_threshold,
                "least_similar_rows": least_similar_rows
            }

    return results
