from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client=Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL="llama-3.1-8b-instant" # or "gpt-4o" or "gpt-4o-mini"