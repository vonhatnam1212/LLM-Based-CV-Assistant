from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from model import langchain_llm

def repharse_user_input(user_input):
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are the assistant tasked with receiving a natural language query from a user and converting it into a query for a vector store. You will take issues related to skills, required skills, work experience, number of years of experience
        Here is the user's query: {question}""",
    )
    llm_chain = LLMChain(llm=langchain_llm, prompt=QUERY_PROMPT)
    repharse_user_input = llm_chain.invoke(user_input)
    print("repharsee user input successful")
    return repharse_user_input
