import json
import sys
import chromadb
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "darshan"
BATCH = 64

def main(chunks_path, chroma_dir):
    client = chromadb.PersistentClient(path=chroma_dir)

    # Recreate collection cleanly each time
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted old collection '{COLLECTION_NAME}'")
    except Exception:
        pass

    col = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    ids, texts, metas = [], [], []
    total = 0
    skipped = 0

    with open(chunks_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            c = json.loads(line)
            
            text = str(c.get("text", "")).strip()
            
            # Skip chunks that are too short to be useful
            if len(text) < 100:
                skipped += 1
                continue

            ids.append(str(c["chunk_id"]))
            texts.append(text)
            metas.append({
                "url": str(c.get("url") or ""),
                "title": str(c.get("title") or ""),
                "published_date": str(c.get("published_date") or ""),
                "doc_id": str(c.get("doc_id") or ""),
            })

            if len(ids) >= BATCH:
                embs = model.encode(
                    texts,
                    batch_size=BATCH,
                    normalize_embeddings=True,
                    show_progress_bar=False,
                ).tolist()

                col.add(ids=ids, documents=texts, metadatas=metas, embeddings=embs)
                total += len(ids)
                print(f"  Indexed {total} chunks...", end="\r")
                ids, texts, metas = [], [], []

    if ids:
        embs = model.encode(
            texts,
            batch_size=BATCH,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).tolist()

        col.add(ids=ids, documents=texts, metadatas=metas, embeddings=embs)
        total += len(ids)

    print(f"\n✅ Indexed {total} chunks into collection '{COLLECTION_NAME}' at {chroma_dir}")
    if skipped:
        print(f"   Skipped {skipped} chunks (too short)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/build_chroma.py <chunks.jsonl> <chroma_dir>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])