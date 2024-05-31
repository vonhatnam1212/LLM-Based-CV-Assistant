from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

def repharse_user_input(user_input,llm):
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are the assistant tasked with receiving a natural language query from a user and converting it into a query for a vector store. You will take issues related to skills, required skills, work experience, number of years of experience
        Here is the user's query: {question}""",
    )
    llm_chain = LLMChain(llm=llm, prompt=QUERY_PROMPT, verbose=True)
    print(llm_chain)
    try:
        repharse_user_input = llm_chain.invoke(user_input)
    except:
        print("error")
    print("repharsee user input successful")
    return repharse_user_input
