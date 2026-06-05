from app.services.chunking.text_chunker import chunk_text

sample_text = """
This is a very long text.
""" * 1000

chunks = chunk_text(sample_text)

print("Chunks:", len(chunks))

for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i+1}")
    print(chunk[:200])