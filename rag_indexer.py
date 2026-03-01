import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAIEmbeddings
from google.cloud import storage

# Configuration
PROJECT_ID = "indigoifs"
LOCATION = "us-central1"
BUCKET_NAME = "indigoifs-rag-test-data"
DATA_FILE = "data/hr_policy.txt"
EMBEDDINGS_FILE = "embeddings.json"

def main():
    print("1. Reading document...")
    with open(DATA_FILE, "r") as f:
        text = f.read()

    print("2. Chunking document...")
    # Chunk the text so we have smaller, manageable pieces to embed
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
    )
    chunks = text_splitter.split_text(text)
    print(f"   Created {len(chunks)} chunks.")

    print("3. Generating embeddings...")
    # Initialize the Vertex AI Embedding model
    embeddings_model = VertexAIEmbeddings(
        model_name="text-embedding-004", 
        project=PROJECT_ID, 
        location=LOCATION
    )
    
    # Store chunks to a local mapping (useful for the agent later)
    # We will write out both the Vector Search format and a metadata format
    vector_search_data = []
    chunk_metadata = {}
    
    for i, chunk in enumerate(chunks):
        # Generate the embedding vector
        vector = embeddings_model.embed_query(chunk)
        chunk_id = f"chunk_{i}"
        
        # Vertex AI Vector Search format: {"id": "str", "embedding": [float]}
        vector_search_data.append({
            "id": chunk_id,
            "embedding": vector
        })
        
        # We also want to save the raw text mapped to the ID so our LLM can read it
        chunk_metadata[chunk_id] = chunk

    print("4. Saving files locally...")
    # Save the embeddings in JSONL format for Vector Search
    with open(EMBEDDINGS_FILE, "w") as f:
        for item in vector_search_data:
            f.write(json.dumps(item) + "\n")
            
    # Save the chunk mapping for our Agent to use
    with open("chunk_metadata.json", "w") as f:
        json.dump(chunk_metadata, f, indent=2)

    print("5. Uploading files to Google Cloud Storage...")
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    
    # Upload embeddings to a specific folder so Vector Search can find them easily
    blob_embeddings = bucket.blob(f"embeddings/{EMBEDDINGS_FILE}")
    blob_embeddings.upload_from_filename(EMBEDDINGS_FILE)
    print(f"   Uploaded {EMBEDDINGS_FILE} to gs://{BUCKET_NAME}/embeddings/")
    
    # Upload chunk metadata
    blob_metadata = bucket.blob("metadata/chunk_metadata.json")
    blob_metadata.upload_from_filename("chunk_metadata.json")
    print(f"   Uploaded chunk_metadata.json to gs://{BUCKET_NAME}/metadata/")

    print("Done! The data is prepared and in GCS.")

if __name__ == "__main__":
    main()
