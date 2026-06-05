from sentence_transformers import SentenceTransformer

model = None


def get_model():
    global model

    if model is None:
        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    return model


def generate_embedding(text: str):

    embedding = get_model().encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()
