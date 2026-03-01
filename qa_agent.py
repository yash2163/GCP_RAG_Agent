import vertexai
from vertexai.preview import rag
from vertexai.preview.generative_models import GenerativeModel, Tool

# Configuration
PROJECT_ID = "indigoifs"
LOCATION = "us-west1"
MODEL_ID = "gemini-1.5-pro-001"

def main():
    print("1. Initializing Vertex AI...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # Read the corpus name from the previous step
    try:
        with open("corpus_name.txt", "r") as f:
            corpus_name = f.read().strip()
    except FileNotFoundError:
        print("Error: corpus_name.txt not found. Did you run create_rag_corpus.py first?")
        return

    print(f"2. Linking Gemini to RAG Corpus: {corpus_name}")
    # Create a Retrieval tool that uses our RAG Corpus
    rag_retrieval_tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_corpora=[corpus_name],
                similarity_top_k=2 # Number of chunks to retrieve
            ),
        )
    )

    # Initialize the Generative Model with the RAG tool
    model = GenerativeModel(
        model_name=MODEL_ID,
        tools=[rag_retrieval_tool],
    )

    print("\n--- Agent is Ready! ---")
    print("Welcome to the MinfyHR Test Agent. Type 'exit' to quit.")
    
    while True:
        query = input("\nAsk me about the HR Policy: ")
        if query.lower() in ['exit', 'quit']:
            break
            
        if not query.strip():
            continue
            
        print("\nThinking...")
        
        # Send the query to Gemini. Gemini will automatically use the RAG tool 
        # to search the corpus, append the context, and answer.
        response = model.generate_content(query)
        
        print("\n--- Response ---")
        print(response.text)
        print("----------------\n")

if __name__ == "__main__":
    main()
