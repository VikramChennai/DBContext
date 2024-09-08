from Embedding.embeddings import TransformerEmbeddingModel, process_csv_embeddings, compare_embeddings

def test_transformer_model():
    model = TransformerEmbeddingModel()
    col_embs = process_csv_embeddings('names.csv', model)
    description_embs = {"Name": model.get_embeddings(["First name of student."])}
    print(col_embs)
    lowest_indices, sim_matrix = compare_embeddings(col_embs, description_embs)
    print(lowest_indices, sim_matrix)
    print("TransformerEmbeddingModel test passed")


if __name__ == "__main__":
    test_transformer_model()
