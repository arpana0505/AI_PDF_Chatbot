# loads the PDFs.

#import class called PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

# take in a string file path and return list of documents
def load_pdf(file_path : str) -> list[Document]:
    # load pdf and return a document per page

    # tell python here is the pdf to load
    loader = PyPDFLoader(file_path)

    # pdf opened, each page read, text extracted, Langchain creates Document objects
    documents = loader.load()

    if not documents:
        raise ValueError(f"No text could be loaded from {file_path}.")
    
    return documents

"""
# give the first element in list, meaning first page
# .page_content to only print the text on the page
print(documents[0].page_content)

# print the metadata
print(documents[0].metadata)

# inspecting document
print(f"Number of pages: {len(documents)}")

print("\nFirst Page:\n")
# print only first 500 characters
print(documents[0].page_content[:500])

print("\nMetadata:")
print(documents[0].metadata)

"""