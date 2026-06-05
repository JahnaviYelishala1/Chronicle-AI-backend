from app.services.rag.search_service import (
    search_chunks
)

results = search_chunks(
    "What adjectives were discussed?"
)

print()

for idx, chunk in enumerate(results, start=1):

    print(f"\nResult {idx}\n")

    print(chunk[:300])