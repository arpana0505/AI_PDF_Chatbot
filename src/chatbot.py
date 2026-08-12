# Langchain messages
from langchain_core.messages import(
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langchain_openai import ChatOpenAI
from components.embeddings import create_embeddings
from components.loader import load_pdf
from components.memory import create_chat_history
from components.splitter import split_documents
from components.vectorstore import (build_vector_store, 
load_vector_store, 
create_retriever)
from config import OPENAI_API_KEY
from utils.helpers import build_context

import os

PDF_PATH = "data/AI_chatbot_makeup.pdf"

# path to Chroma vector db
DATABASE_PATH = "db"


def create_chatbot(pdf_path, database_path):
    # create the PDF retriever, LLM, and chat history

    # loader
    print("Loading PDF...")
    documents = load_pdf(pdf_path)

    # splitter, create chunks
    print("Splitting Document...")
    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    # embeddings
    print("Creating embeddings...")
    embeddings = create_embeddings()

    # check if database folder exists and if it has files inside 
    if os.path.exists(database_path) and os.listdir(database_path):
        print("Loading existing vector databases...")

        vector_store = load_vector_store(
            embeddings = embeddings,
            persist_directory = database_path
        )
    else:
        print("Processing new PDF...")
        doucments = load_pdf(pdf_path)

        print("Splitting document...")
        chunks = split_documents(documents)

        print(f"Created {len(chunks)} chunks.")

        # vector db
        print("Buidling vector database...")
        vector_store = build_vector_store(
            chunks = chunks,
            embeddings = embeddings,
            persist_directory = database_path
        )

    # retrieve top 3 chunks
    retriever = create_retriever(
        vector_store = vector_store,
        number_of_results = 3
    )

    # set up llm
    llm = ChatOpenAI(
        model = "gpt-4.1-mini",
        api_key = OPENAI_API_KEY,
        temperature = 0
    )

    chat_history = create_chat_history()

    return retriever, llm, chat_history

def answer_question(
    question, retriever, llm, chat_history) -> str: 

    # answer one question and update the conversation history.

    # .invoke() executes the retriever function
    # the retriever searches for the top 3 chunks
    retrieved_documents = retriever.invoke(question)

    # join all the chunks
    context = build_context(retrieved_documents)

    # include the context and question in the prompt
    # create a copy of the chat history and append it with the most reccent user question
    messages = chat_history.copy()

    messages.append(
        HumanMessage(
            content = f"""
            Dcoument Context:

            {context}

            Current Question:

            {question}
            """
        )
    )
    
    # send message to LLM
    response = llm.invoke(messages)

    answer = response.content

    # save user question 
    chat_history.append(
        HumanMessage(content = question)
    )

    # save AI response
    chat_history.append(
        AIMessage(content = answer)
    )

    return answer

def run_chatbot() -> None:

    retriever, llm, chat_history = create_chatbot(pdf_path)

    print("\nPDF Chatbot is ready")
    print("Type 'exit' to stop the program.")


    # ask question in loop
    while True:
        question = input("\nYou: ").strip()

        # change to all lowercases before checking
        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue


        answer = answer_question(
            question = question,
            retriever = retriever,
            llm = llm,
            chat_history = chat_history
        )

        # display response
        print(f"\nAI: {answer}")

if __name__ == "__main__":
    run_chatbot()


