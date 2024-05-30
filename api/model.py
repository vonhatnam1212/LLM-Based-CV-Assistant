import sys
import os
sys.path.append("../api")
from config import (
    PINECONE_API_KEY,
    GOOGLE_API_KEY,
    OPENAI_API_KEY,
    COHERE_API_KEY,
)

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["COHERE_API_KEY"] = COHERE_API_KEY
from pinecone import Pinecone
from langchain.chat_models import ChatOpenAI
from llama_index.llms.gemini import Gemini
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.postprocessor.cohere_rerank import CohereRerank
from langchain_google_genai import ChatGoogleGenerativeAI

pinecoin = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pinecoin.Index("resume-assistant")
llamaindex_llm = Gemini(model_name="models/gemini-pro")
# define embedding function
llamaindex_embed_model = HuggingFaceEmbedding(model_name="intfloat/multilingual-e5-large-instruct")
llamaindex_cohere_rerank = CohereRerank(top_n=5)

# langchain_llm = ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo-0125")
langchain_llm = ChatGoogleGenerativeAI(model="gemini-pro")