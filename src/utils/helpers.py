from langchain_core.documents import Document

# combine all the retrieved documents into one context string
def build_context(documents: list[Document]) -> str:

    context_parts = []

    for doc in documents:
        page_number = doc.metadata.get("page", "Unknown")
    
        # add 1 to page number since it starts at 0
        if isinstance(page_number, int):
            page_number+=1

        context_parts.append(
            f"Page {page_number}:\n{doc.page_content}"
        )
    
    return "\n\n".join(context_parts)
