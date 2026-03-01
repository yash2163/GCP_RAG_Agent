import vertexai
from vertexai.preview import rag

# Configuration
PROJECT_ID = "indigoifs"
LOCATION = "us-west1"
DOCUMENT_PATH = "data/hr_policy.txt"

def main():
    print(f"Initializing Vertex AI in project '{PROJECT_ID}' and location '{LOCATION}'...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # Read the existing corpus name
    with open("corpus_name.txt", "r") as f:
        corpus_name = f.read().strip()
    
    print(f"Uploading document '{DOCUMENT_PATH}' to Corpus '{corpus_name}' using direct upload...")
    
    # Upload local file directly to RAG Engine
    response = rag.upload_file(
        corpus_name=corpus_name,
        path=DOCUMENT_PATH,
        display_name="hr_policy.txt"
    )
    
    print("✅ Document uploaded successfully!")
    print(f"Upload response: {response}")

if __name__ == "__main__":
    main()
