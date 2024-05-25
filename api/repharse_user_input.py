import os
import openai
import sys
import logging

sys.path.append("../api")
from config import PINECONE_API_KEY, GOOGLE_API_KEY, OPENAI_API_KEY, COHERE_API_KEY

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["COHERE_API_KEY"] = COHERE_API_KEY
import phoenix as px

# embedding
from pinecone import Pinecone

# langchain
from langchain.llms import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI


def repharse_user_input(user_input):
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are the assistant tasked with receiving a natural language query from a user and converting it into a query for a vector store. You will take issues related to skills, required skills, work experience, number of years of experience
        Here is the user's query: {question}""",
    )
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    llm_chain = LLMChain(llm=llm, prompt=QUERY_PROMPT)
    repharse_user_input = llm_chain.invoke(user_input)
    print("repharsee user input successful")
    return repharse_user_input
