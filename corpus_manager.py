import vertexai
from vertexai.preview import rag
import sys
import os

# Configuration
PROJECT_ID = "indigoifs"
LOCATION = "us-west1"

def init_rag():
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    try:
        with open("corpus_name.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("❌ Error: corpus_name.txt not found. Root corpus must be created first.")
        sys.exit(1)

def list_documents(corpus_name):
    print(f"\n--- Documents in Corpus: {corpus_name} ---")
    # List files in the corpus
    files = rag.list_files(corpus_name=corpus_name)
    count = 0
    for f in files:
        print(f"📄 ID: {f.name.split('/')[-1]} | Name: {f.display_name}")
        count += 1
    if count == 0:
        print("No documents found.")
    print("------------------------------------------\n")

def upload_document(corpus_name, file_path):
    if not os.path.exists(file_path):
        print(f"❌ Error: File {file_path} not found.")
        return
    
    print(f"📤 Uploading {file_path}...")
    response = rag.upload_file(
        corpus_name=corpus_name,
        path=file_path,
        display_name=os.path.basename(file_path)
    )
    print(f"✅ Uploaded! File ID: {response.name.split('/')[-1]}")

def clean_corpus(corpus_name):
    print(f"⚠️ Warning: This will delete ALL documents in {corpus_name}.")
    confirm = input("Are you sure? (y/N): ")
    if confirm.lower() == 'y':
        files = rag.list_files(corpus_name=corpus_name)
        for f in files:
            print(f"🗑️ Deleting {f.display_name}...")
            rag.delete_file(name=f.name)
        print("✨ Corpus cleaned.")
    else:
        print("Operation cancelled.")

def print_help():
    print("""
Usage: python3 corpus_manager.py [command] [args]
Commands:
  list              - List all documents in the corpus
  add [file_path]   - Add a new document (txt or pdf)
  clean             - Delete all documents in the corpus
    """)

if __name__ == "__main__":
    corpus_id = init_rag()
    
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)
        
    cmd = sys.argv[1].lower()
    
    if cmd == "list":
        list_documents(corpus_id)
    elif cmd == "add":
        if len(sys.argv) < 3:
            print("❌ Error: Please specify a file path.")
        else:
            upload_document(corpus_id, sys.argv[2])
    elif cmd == "clean":
        clean_corpus(corpus_id)
    else:
        print_help()
