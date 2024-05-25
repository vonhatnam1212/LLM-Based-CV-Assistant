import os
import openai
import sys
sys.path.append("../api")
from config import PINECONE_API_KEY, GOOGLE_API_KEY, OPENAI_API_KEY, COHERE_API_KEY

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["COHERE_API_KEY"] = COHERE_API_KEY
from langchain_community.callbacks import get_openai_callback

from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI
from retrieval import get_query_engine
from repharse_user_input import repharse_user_input
from get_documents import get_documents
llm = ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo-0125")
def get_documents_query(user_input):
    repharse_user = repharse_user_input(user_input)
    query = get_query_engine().query(repharse_user["question"])
    file_name = []
    for key in query.metadata:
        file_name.append(query.metadata[key]["file_name"])

    origin_document = get_documents("/home/nam/workspace/LLMs/LLM-Based-CV-Assistant/data/extract_CV.jsonl")
    query_document = []
    for doc in origin_document:
        if doc["metadata"]["file_name"] in file_name:
            query_document.append(doc)
    print("get documents query successful")
    return repharse_user,query_document, file_name

def get_chains():
    prompt = ChatPromptTemplate.from_template(
        "With this {requirement}, please compare the following CVs and state why these CVs are suitable for these requirements:"
        + "\n\n{resume_doc1} + \n{resume_doc2} + \n{resume_doc3} + \n{resume_doc4} + \n{resume_doc5}"
    )
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        output_key="result",
        verbose=True,
    )
    return llm_chain


def get_query(repharse_user_input,query_document, llm):
    llm_chain = get_chains()
    
    overall_chain = SequentialChain(
        chains=[llm_chain],
        input_variables=[
            "requirement",
            "resume_doc1",
            "resume_doc2",
            "resume_doc3",
            "resume_doc4",
            "resume_doc5",
        ],
        output_variables=["result"],
        verbose=True,
    )

    seqchain_output = overall_chain({"requirement":repharse_user_input["question"],"resume_doc1":query_document[0]["overview_CV"],"resume_doc2":query_document[1]["overview_CV"],"resume_doc3":query_document[2]["overview_CV"],"resume_doc4":query_document[3]["overview_CV"],"resume_doc5":query_document[4]["overview_CV"]})
    print("get_query successfu;")
    return seqchain_output

def user_query(user_input):
    question, documents, file_name_document = get_documents_query(user_input)
    with get_openai_callback() as cb:
        query = get_query(question, documents, llm)
    print("ALL sucessful")
    return query, cb, file_name_document

# question, documents = get_documents_query("""1. Educational Qualifications
#     • Bachelor’s degree in Computer Science, Engineering, Mathematics or related field of study
# 2. Relevant Knowledge/ Expertise
#     • 5-10 years experiences in software development and at least 3 years in banking and fintech domain.
#     • An understanding of bank business processes, fintech solution and constraints.
# 3. Relevant Experience
#     • Expert in JAVA language, Spring boot, Hibernate, jpa, and solid work with IDE
#     • Net Framework should be considered added skill.
#     • Advanced Knowledge MS SQL, Oracle DBs
#     • Having knowledge about microservice, Kubernetes, ability to config EKS.
#     • Experience with source code management like Git, Gitlab, Jira.
#     • Good understanding on webservice SOAP/Restful, Standard message JSON, XML, OOP, Design pattern ...
#     • Knowledge on Angular, JS is big plus.
# 4. Skill
#     • Ability in English reading and writing (mandatory), and speaking, listening (preferable).
# 5. Others
#     • Teamwork, careful, attention to detail, logical thinking.
#     • Problem-solving skills, ability to work under high pressure and can-do attitude.
#     • Self-development and motivation skill.
# """)
# print(question,documents)