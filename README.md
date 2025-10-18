# MongoDB + Hugging Face Vector Search

This project demonstrates how to:
- Connect to MongoDB Atlas
- Generate embeddings with Hugging Face (`all-MiniLM-L6-v2`)
- Store embeddings in MongoDB
- Perform semantic vector search using `$vectorSearch`

---

## Features
- End-to-end example of semantic search with MongoDB
- Uses Hugging Face Sentence Transformers for embeddings
- Environment-based configuration for easy setup
- Simple Python interface to add embeddings and run queries

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/wafadalilahabet-jpg/mongo-hf-vectorsearch.git
cd mongo-hf-vectorsearch
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
# Activate on Linux/Mac
source venv/bin/activate
# Activate on Windows
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pymongo python-dotenv sentence-transformers
```

### 4. Configure environment variables
Copy the example file and update your MongoDB credentials:
```bash
cp .env.example .env
```

Edit `.env`:
```bash
MONGO_URI="your-mongodb-connection-uri"
MONGO_DB="sample_mflix"
MONGO_COLLECTION="movies"
```

---

## Usage

Run the main script:
```bash
python app.py
```

Inside `app.py`, you can:

```python
# Add embeddings to documents (only if missing)
add_embeddings()

# Perform a semantic search
vector_search("imaginary character from outer space at war")
```

### Expected Output
```text
Star Wars
Luke Skywalker joins forces with a Jedi Knight...

Guardians of the Galaxy
A group of intergalactic criminals must pull together...
```

---

## Project Structure
```
mongo-hf-vectorsearch/
│── app.py                # Main script
│── requirements.txt       # Python dependencies
│── .env.example           # Example environment variables
│── README.md              # Project documentation
```

---

## Requirements
- Python 3.8+
- MongoDB Atlas cluster (with vector search enabled)
- Hugging Face Sentence Transformers

⚠️ Make sure you have created a vector search index in your MongoDB collection:
- Path: plot_embedding_hf
- Type: vector
- Dimensions: 384 (for `all-MiniLM-L6-v2`)
- Similarity: cosine


