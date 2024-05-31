import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY", "input GEMINI")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "input PINECONE_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "input OPENAI")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY", "input CHORE")
LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_API_KEY","input LANGCHAIN KEY")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID","input AWS acess key")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY","input AWS secret key")
FILE_PATH = "../data/extract_CV.jsonl"