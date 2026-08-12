# UI - Streamlit

import os

import streamlit as st
from chatbot import answer_question, create_chatbot
from components.memory import create_chat_history

import hashlib

# configure webpage, browser tab title
st.set_page_config(
    page_title = "AI PDF Chatbot",
    layout="centered"
)

st.title("AI PDF Chatbot")
st.caption("Upload a PDF and ask questions about its contents.")


# # force the retriever to be initialized only once in the beginning
# # if the chatbot is not in the session state then build it, if it is then reuse it
# if "retriever" not in st.session_state:
#     # add a loading spinner, so while the code inside is running, ..
#     # users see the loading sign and text
#     with st.spinner("Preparing the PDF knowledge base..."):
#         retriever, llm, chat_history = create_chatbot()

#         # store the retriever, llm, chat history in streamlit's backpack
#         st.session_state.retriever = retriever
#         st.session_state.llm = llm
#         st.session_state.chat_history = chat_history

#----------------------------------
#SIDEBAR
#-------------------------------------

with st.sidebar:

    # pdf
    st.header("Document")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type = ["pdf"]
    )
    
    st.divider()

    # clear convo
    st.header("Controls")

    if st.button("Clear conversation"):
        if "chat_history" in st.session_state:
            st.session_state.chat_history = create_chat_history()

        st.session_state.display_messages = [
            {
                "role": "assistant",
                "content": ("Conversation cleared! "
                "Ask me another question about the PDF.")
            }
        ]
        st.rerun()


#----------------------------------
#DISPLAY MESSAGE HISTORY
#-------------------------------------

# another variable inside the backpack
if "display_messages" not in st.session_state:
    st.session_state.display_messages = [
        # dictionaries tell Streamlit for draw these messages on the screen
        {
            "role" : "assistant",
            "content" : ("Hello! Upload a PDF and ask me a question about it.")
        }
    ]


#----------------------------------
#PROCESS UPLOADED PDF
#----------------------------------

if uploaded_file:

    # calculate unique ID from the actual file contents
    file_bytes = uploaded_file.getvalue()

    # create unique fingerprint for the uploaded pdf
    # run PDF's bytes through SHA-356 hashing alg
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    # check whether it is a new PDF
    current_file_hash = st.session_state.get(
        "uploaded_file_hash"
    )

    if current_file_hash != file_hash:

        # forget previous pdf and conversation
        st.session_state.pop("retriever", None)
        st.session_state.pop("llm", None)
        st.session_state.pop("chat_history", None)

        with st.spinner("Reading and processing your PDF..."):

            # create folder if it doesn't eist
            os.makedirs("data/uploads", exist_ok = True)

            # join multiple folder and file names to make one complete path
            temp_path = os.path.join(
                "data",
                "uploads",
                uploaded_file.name
            )

            # save uploaded PDF to disk temporarily
            # wb = write binary
            with open(temp_path, "wb") as file:
                # get the raw PDF bytes
                file.write(file_bytes)

            # unique vector db for this pdf
            database_path = os.path.join(
                "db", file_hash
            )

            # create chatbot for THIS pdf
            retriever, llm, chat_history = (
                create_chatbot(
                    pdf_path = temp_path,
                    database_path = database_path
                    )
            )

            # save chatbot state
            st.session_state.retriever = retriever
            st.session_state.llm = llm
            st.session_state.chat_history = (
                chat_history
            )
            st.session_state.uploaded_file_hash = (file_hash)

            st.session_state.uploaded_filename = (
                uploaded_file.name
            )
            
            # update the file name because using new PDF
            st.session_state.display_messages = [
                {
                    "role": "assistant",
                    "content": (
                            f"{uploaded_file.name} is ready! Ask me a question about it."
                        
                    )
                }
            ]

            st.success(
                f"{uploaded_file.name} processed successfully!"
            )


#----------------------------------
#SHOW PREVIOUS CHAT
#----------------------------------


# display all messages
for message in st.session_state.display_messages:
    # chat message creates one big chat bubble
    # assign each bubble to either the AI assistant bubble or user bubble
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


#----------------------------------
#CHAT INPUT
#----------------------------------

# displaying chat input in the bottom of the page
question = st.chat_input("Ask a question about the PDF")

#----------------------------------
#HANDLING QUESTION
#----------------------------------

# if user types somethings then run the chatbot
if question:
    st.session_state.display_messages.append(
        {
        "role": "user",
        "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)
    
    with st.chat_message("assistant"):
        with st.spinner("Searching the document..."):
            try:
                answer = answer_question(
                    question = question,
                    # get from Streamlit backpack
                    retriever = st.session_state.retriever,
                    llm = st.session_state.llm,
                    chat_history = st.session_state.chat_history
                )
                st.markdown(answer)
            
            except Exception as error:
                answer = ("I encountered an error while answering your question.")
                st.error(answer)
                print(f"Chatbot error: {error}")
    # save chatbot answers
    st.session_state.display_messages.append(
        {
        "role": "assistant",
        "content": answer
        }
    )


