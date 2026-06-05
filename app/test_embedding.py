from app.services.embeddings.embedding_service import (
    generate_embedding
)

vector = generate_embedding(
    "Hello world"
)

print(len(vector))
print(vector[:5])