
# import a function that reads the env. file
from dotenv import load_dotenv

# os module allow Python to interact with the operating system, it can read env variables
import os

# read env file and loads everything into memory
load_dotenv()

# is there an environment variable callsed OPEN_AI_API?, if yes it returns its value
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY was not found. "
        "Make sure it is defined in your .env file."
    )



