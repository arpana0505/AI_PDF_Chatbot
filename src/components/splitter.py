# handle chunking

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(
    documents: list[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200) -> list[Document]:

    # create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,

        # overlaps 200 characters from previous chunk
        chunk_overlap = chunk_overlap
    )

    # insert documents as parameter in the split_doc function from text_splitter module
    chunks = text_splitter.split_documents(documents)
    
    return chunks









# # loading the PDF
# loader = PyPDFLoader("data/AI_chatbot_makeup.pdf")
# documents = loader.load()



"""
print(f"Original pages: {len(documents)}")
print(f"Chunks created: {len(chunks)}")

print("\nFirst chunk:\n")
print(chunks[0].page_content)

print("\nMetadata:")
print(chunks[0].metadata)
"""