"""
MongoDB + Hugging Face Embeddings + Vector Search
=================================================

This script demonstrates how to:
1. Connect to MongoDB.
2. Generate embeddings for movie plots using Hugging Face's `sentence-transformers`.
3. Store embeddings in MongoDB.
4. Perform semantic vector search using MongoDB's `$vectorSearch`.

Requirements:
- Python 3.10+
- MongoDB Atlas with a vector index
- Environment variables in a `.env` file:
    MONGO_URI=<your-mongodb-uri>
    MONGO_DB=sample_mflix
    MONGO_COLLECTION=movies
"""

import os
import pymongo
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


# ------------------------- Step 1: Load environment variables -------------------------
load_dotenv()  # Load variables from .env file

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "sample_mflix")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "movies")


# ------------------------- Step 2: Connect to MongoDB -------------------------
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
print("[INFO] Connected to MongoDB")


# ------------------------- Step 3: Load Hugging Face embedding model -------------------------
hf_model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings_hf(text: str) -> list[float]:
    """
    Generate embeddings from text using Hugging Face model.
    
    Args:
        text (str): Input text to encode.
    
    Returns:
        list[float]: Embedding vector.
    """
    return hf_model.encode(text).tolist()


# ------------------------- Step 4: Add embeddings to documents -------------------------
def add_embeddings(limit: int = 50) -> None:
    """
    Generate and store embeddings for movie plots that do not yet have them.
    
    Args:
        limit (int): Number of documents to process.
    """
    cursor = collection.find(
        {"plot": {"$exists": True}, "plot_embedding_hf": {"$exists": False}}
    ).limit(limit)

    count = 0
    for doc in cursor:
        embedding = generate_embeddings_hf(doc["plot"])
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"plot_embedding_hf": embedding}},
        )
        count += 1
    
    print(f"[INFO] Added {count} new embeddings")


# ------------------------- Step 5: Vector search -------------------------
def vector_search(query: str, limit: int = 4) -> None:
    """
    Perform semantic vector search on the MongoDB movie collection.
    
    Args:
        query (str): Search query text.
        limit (int): Number of results to return.
    """
    query_embedding = generate_embeddings_hf(query)
    
    results = collection.aggregate(
        [
            {
                "$vectorSearch": {
                    "queryVector": query_embedding,
                    "path": "plot_embedding_hf",
                    "numCandidates": 100,
                    "limit": limit,
                    "index": "PlotSemanticSearch",
                }
            }
        ]
    )

    print(f"\n[RESULTS] Top {limit} matches for query: '{query}'\n")
    for doc in results:
        print(f"- {doc['title']}\n  {doc['plot']}\n")


# ------------------------- Main -------------------------
if __name__ == "__main__":
    add_embeddings()
    vector_search("imaginary character from outer space at war")
