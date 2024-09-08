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
    df = pd.read_csv(csv_filename)
    header_embedding = embedding_model.get_embeddings([' '.join(df.columns)])[0]
    column_embeddings = {column: embedding_model.get_embeddings(df[column].astype(str).tolist()) for column in df.columns}

    output_filename = f"{csv_filename.split('.')[0]}_embeddings.pt"
    torch.save({
        'header_embedding': header_embedding,
        'column_embeddings': column_embeddings
    }, output_filename)
    print(f"Embeddings saved to '{output_filename}'")
    return header_embedding, column_embeddings

# Example usage
transformer_model = TransformerEmbeddingModel()
header_emb, col_embs = process_csv_embeddings('test_file.csv', transformer_model)

# openai_model = OpenAIEmbeddingModel()
# header_emb, col_embs = process_csv_embeddings('test_file.csv', openai_model)
