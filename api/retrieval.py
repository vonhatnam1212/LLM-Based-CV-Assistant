import os
import openai
import sys

sys.path.append("../api")
from config import PINECONE_API_KEY, GOOGLE_API_KEY, OPENAI_API_KEY, COHERE_API_KEY

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["COHERE_API_KEY"] = COHERE_API_KEY
from pinecone import Pinecone

# langchain
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.retrievers import RePhraseQueryRetriever

# llamaindex
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import IndexNode
from llama_index.core.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
)
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.gemini import Gemini
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, get_response_synthesizer
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core import StorageContext
from get_documents import get_documents

pinecoin = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pinecoin.Index("resume-assistant")
llm = Gemini(model_name="models/gemini-pro")
# define embedding function
embed_model = HuggingFaceEmbedding(model_name="intfloat/multilingual-e5-large-instruct")
Settings.chunk_size = 512


def save_index_vectordb():
    origin_documents = get_documents(
        "/home/nam/workspace/LLMs/LLM-Based-CV-Assistant/data/extract_CV.jsonl"
    )
    from llama_index.core import Document

    documents = []
    for document in origin_documents:
        documents.append(
            Document(
                text=document["overview_CV"],
                metadata=document["metadata"],
            )
        )
    # Không chạy cell này mà chạy cell dưới (cái này dùng để tạo vector db)
    # Create an index over the documnts
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,
        embed_model=embed_model,
    )
    return index


def load_index_vectordb():
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store, show_progress=True, embed_model=embed_model
    )

    return index


def get_query_engine():
    try:
        cohere_rerank = CohereRerank(top_n=5)

        index = load_index_vectordb()
        # configure retriever
        retriever = VectorIndexRetriever(
            index,
            verbose=True,
            similarity_top_k=5,
        )

        # assemble query engine
        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            node_postprocessors=[cohere_rerank],
        )
        print("query engine successful")
    except:
        print("error query engine")
    return query_engine
