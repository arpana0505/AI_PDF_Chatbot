# everytime chatbot starts create a fresh conversation history

from langchain_core.messages import SystemMessage
from components.prompt import SYSTEM_INSTRUCTIONS

# reurning a list since multiple messages in order
def create_chat_history() -> list:
    return [
        SystemMessage(content = SYSTEM_INSTRUCTIONS)
        ]