from db_manager import save_post, search_similar

# --- GUARDAR UN POST DE PRUEBA ---
print("Saving a test post in Pinecone...")
save_post(
    text="How to create engaging content on LinkedIn in 2025.",
    prompt="Generate a post about engaging LinkedIn content.",
    platform="LinkedIn",
    tone="Professional",
    company="FutureCorp",
    language="English",
    audience="Business professionals",
    model="mistralai/mistral-7b-instruct",
    image_url="https://example.com/image.png"
)

# --- BUSCAR POSTS SIMILARES ---
print("\nSearching for similar posts...")
results = search_similar("engaging LinkedIn content", top_k=2)
for doc, score in results:
    print(f"\n---\nScore: {score:.3f}")
    print("Text:", doc.page_content)
    print("Metadata:", doc.metadata)
