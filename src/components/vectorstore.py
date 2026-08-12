# loader, splitter, embeddings, vector database
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


def build_vector_store(
    chunks: list[Document],
    embeddings: OpenAIEmbeddings,
    persist_directory: "db") -> Chroma:

    return Chroma.from_documents(
        documents = chunks,
        embedding = embeddings,

        # persist_directory allows embeddings to be saved to disk
        persist_directory = persist_directory
    )

def load_vector_store(
    embeddings, persist_directory):
    # load an existing Chroma vector store

    return Chroma(
        persist_directory = persist_directory,
        embedding_function = embeddings
    )


def create_retriever(
    vector_store: Chroma,
    number_of_results: int = 3,):
    #Create a retriever that returns the most relevant chunks.

    return vector_store.as_retriever(
        search_kwargs={"k": number_of_results}
    )



# # load the PDF
# loader = PyPDFLoader("data/AI_chatbot_makeup.pdf")
# documents = loader.load()

# # split the text
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 1000,
#     chunk_overlap = 200
# )

# chunks = text_splitter.split_documents(documents)

# # embedding model
# embeddings = OpenAIEmbeddings(
#     model = "text-embedding-3-small",
#     api_key = OPENAI_API_KEY
# )


# query = "How should one properly read the news?"

# results = vector_store.similarity_search(
#     query,
#     k = 3 # give the 3 most similar chunks
# )

# print(results[0].page_content)