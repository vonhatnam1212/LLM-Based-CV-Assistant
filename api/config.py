import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY", "input GEMINI")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "input PINECONE_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "input OPENAI")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY", "input CHORE")
FILE_PATH = "../data/extract_CV.jsonl"