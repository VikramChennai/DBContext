import torch
import pandas as pd
from abc import ABC, abstractmethod

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
