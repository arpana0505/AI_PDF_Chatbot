# Document RAG Assistant

An AI-powered document answering question answering application built with Retrieval-Augmented Generation (RAG). Users can upload a PDF, ask questions about its contents, and receive responses based on relevant information retrieved directly from the document. 

The application combines semantic search, vector embeddings, conversational memory, and an LLM to provide context-aware answers while reducing responses based on information outside the uploaded document. 

## Live Demo

Try the application: https://pdf-assistant-ai.streamlit.app/

## Key Features

* PDF Upload: Upload a interact with different PDF documents through a Streamlit interface.
* RAG: Retrieves relevant sections of the documents before generating a response.
* Semantic Search: Uses vector embeddings and Chroma to find document chunks based on meaning rather than exact keyword matches.
* Document Grounding: Instructs the model to answer using information retrieved from the uploaded document and provide page references.
* Conversational Memory: Maintains previous questions and responses during a conversation
* Document Isolation: Uses SHA-256 hashing to identify PDFs and maintain separate vector stores for different documents.
* Vector Store Caching: Reuses previously generated embeddings when the same PDF is uploaded again, reducing processing time and API usage.
* Document Switching: Automatically resets the active retriever and conversation when a different PDF is uploaded.
* Interactive UI: Provides document upload, chat history, loading indicators, and conversation controls through Streamlit.

## Architecture

![Document Rag Assistant Architecture](assets/architecture.png)

## Rag Pipeline

1. Document Loading
The uploaded PDF is loaded and its text and page metadata are extracted.

2. Text Chunking
The document is divided into smaller overlapping chunks so relevant sections can be retrieved independently.

3. Embedding Generation
Each chunk is converted into a vector embedding that represents its semantic meaning.

4. Vector Storage
The embeddings and associated document chunks are stored in Chroma for similarity-based retrieval.

5. Semantic Retrieval
When the user asks a question, the question is embedded and compared against the stored vectors to retrieve the most relevant document chunks.

6. Context-Augmented Generation
The retrieved chunks, page information, conversation history, and current question are provided to the LLM as context.

7. Grounded Response
The LLM generates an answer using the retrieved document context and can reference the pages containing the supporting information.

## Document Caching

Each uploaded PDF is identified using a SHA-256 hash of its contents:

PDF → SHA-256 Hash → Unique Chroma Database

If the same PDF is uploaded again, the application detects the matching hash and loads its existing vector store rather than rebuilding all document embeddings.

Different PDFs receive different database paths, preventing embeddings from separate documents from being mixed.
