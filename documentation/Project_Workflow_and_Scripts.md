# Project Workflow & Script Guide

This guide details the specific files in this repository, their purposes, and the order in which they should be used to manage and interact with the RAG agent.

---

## 📂 File Directory & Purpose

### 1. `create_rag_corpus.py` (The Initializer)
*   **Purpose:** A one-time setup script. It contacts Google Cloud to create a permanent "Corpus" (a managed vector database/storage hybrid).
*   **Usage:** You only run this **once** for the life of the project. 
*   **Output:** It saves the unique GCP resource ID into `corpus_name.txt`.

### 2. `corpus_manager.py` (The Data Orchestrator)
*   **Purpose:** Your day-to-day utility tool for managing the knowledge base.
*   **Capabilities:**
    *   `python3 corpus_manager.py list`: Displays all files currently indexed in the GCP Corpus.
    *   `python3 corpus_manager.py add [path]`: Ingests and embeds a new document (e.g., `.txt` or `.pdf`).
    *   `python3 corpus_manager.py clean`: Deletes all documents from the corpus (useful for resets or clearing old data).

### 3. `qa_agent.py` (The Client)
*   **Purpose:** The interactive RAG Chatbot CLI.
*   **Logic:** It reads the Corpus ID from `corpus_name.txt`, links Gemini to that data pool via a Retrieval Tool, and generates answers based exclusively on your managed documents.

### 4. `rag_indexer.py` (The Learning Reference)
*   **Purpose:** This was the "Low-level" or "Stage 1" script. It demonstrates how text chunking and embedding generation works manually.
*   **Usage:** You don't need to run this for the active Vertex RAG workflow, but it is excellent for understanding the underlying mechanics of vector search.

---

## 🔄 Recommended Execution Order

If you are starting a new project or resetting your data, follow this sequence:

### Step 1: Initialize (One-time)
Create the infrastructure on Google Cloud.
```bash
python3 create_rag_corpus.py
```

### Step 2: Manage Data (Anytime)
Population and verification of your knowledge base.
*   **Check existing files:**
    ```bash
    python3 corpus_manager.py list
    ```
*   **Add new knowledge:**
    ```bash
    python3 corpus_manager.py add data/hr_policy.txt
    ```

### Step 3: Chat (The Final Goal)
Interact with your data-aware AI agent.
```bash
python3 qa_agent.py
```

---

## 🧪 Quick Test
You can quickly verify the status of your GCP Corpus by running:
```bash
python3 corpus_manager.py list
```

---
*Created for the GCP RAG Agent Learning Series.*
