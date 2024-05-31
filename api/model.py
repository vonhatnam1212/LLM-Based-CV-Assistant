import sys
import os

sys.path.append("../api")
from config import (
    PINECONE_API_KEY,
    GOOGLE_API_KEY,
    OPENAI_API_KEY,
    COHERE_API_KEY,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY
)

os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["COHERE_API_KEY"] = COHERE_API_KEY
from langchain_community.chat_models.bedrock import BedrockChat
from pinecone import Pinecone
from langchain.chat_models import ChatOpenAI
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.postprocessor.cohere_rerank import CohereRerank
from langchain_community.llms.bedrock import Bedrock
from langchain.callbacks.base import BaseCallbackHandler
from langchain_aws.chat_models.bedrock import ChatBedrock



class BedrockTokenCounter(BaseCallbackHandler):
    def __init__(self, llm):
        self.llm = llm
        self.input_tokens = 0
        self.output_tokens = 0

    def on_llm_start(self, serialized, prompts, **kwargs):
        for p in prompts:
            self.input_tokens += self.llm.get_num_tokens(p)

    def on_llm_end(self, response, **kwargs):
        results = response.flatten()
        for r in results:
            self.output_tokens = self.llm.get_num_tokens(r.generations[0][0].text)


pinecoin = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pinecoin.Index("resume-assistant")
# llamaindex_llm = Gemini(model_name="models/gemini-pro")
# define embedding function
llamaindex_embed_model = HuggingFaceEmbedding(
    model_name="intfloat/multilingual-e5-large-instruct"
)
llamaindex_cohere_rerank = CohereRerank(top_n=5)


def get_langchain_llm(model_name):
    if model_name == "openai":
        langchain_llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo-0125")
    elif model_name == "Llama370BInstruct":
        langchain_llm = ChatBedrock(
            model_id="meta.llama3-70b-instruct-v1:0",
            region_name="ap-south-1",
            model_kwargs={
                "temperature": 0.5,
                # "max_tokens": 4096,
            },  # Set temperature here
        )
    elif model_name == "Mixtral8x7BInstruct":
        langchain_llm = ChatBedrock(
            model_id="mistral.mixtral-8x7b-instruct-v0:1",
            region_name="ap-south-1",
            model_kwargs={
                "temperature": 0.5,
                # "max_tokens": 4096,
            },  # Set temperature here
        )
    elif model_name == "MistralLarge":
        langchain_llm = ChatBedrock(
            model_id="mistral.mistral-large-2402-v1:0",
            region_name="ap-south-1",
            model_kwargs={
                "temperature": 0.5,
                # "max_tokens": 4096,
            },  # Set temperature here
        )
    return langchain_llm
