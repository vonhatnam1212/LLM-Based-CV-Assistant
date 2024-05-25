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
from prompt import templates, ovewview_template

# embedding
from pinecone import Pinecone

# langchain
logging.basicConfig()
logging.getLogger("langchain.retrievers.re_phraser").setLevel(logging.INFO)
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI

import json
from llama_index.core import SimpleDirectoryReader

pinecoin = Pinecone(api_key=PINECONE_API_KEY)

pinecone_index = pinecoin.Index("resume-assistant")

llm = ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo-0125")


def get_origin_documents(file_path):

    reader = SimpleDirectoryReader(input_dir=file_path, recursive=True)
    documents = reader.load_data(show_progress=True)

    return documents


def save_dict_to_jsonl(data, filename):
    with open(filename, "a", encoding="utf-8") as file:
        json_record = json.dumps(data)
        file.write(json_record + "\n")


def get_list_chains(list_templates):
    list_chains = []
    for template_name in list_templates:
        prompt = ChatPromptTemplate.from_template(
            templates[template_name] + "\n\n{resume_doc}"
        )
        list_chains.append(
            LLMChain(
                llm=llm,
                prompt=prompt,
                output_key=template_name,
                verbose=True,
            )
        )
    return list_chains


# viết 1 đoạn summary CV
def write_overview_CV(document, templates, llm, ovewview_template):
    list_chain = get_list_chains(templates)

    # summary CV
    overview_prompt = ChatPromptTemplate.from_template(
        ovewview_template
        + "\n\n{Contact__information}"
        + "\n{CV__summary}"
        + "\n{Work__experience}"
        + "\n{CV__Projects}"
        + "\n{CV__Education}"
        + "\n{candidate__skills}"
        + "\n{CV__Languages}"
        + "\n{CV__Certifications}"
    )
    list_chain.append(
        LLMChain(
            llm=llm,
            prompt=overview_prompt,
            output_key="overview_CV",
            verbose=True,
        )
    )
    overall_chain = SequentialChain(
        chains=list_chain,
        input_variables=["resume_doc"],
        output_variables=list(templates.keys()) + ["overview_CV"],
        verbose=True,
    )

    seqchain_output = overall_chain(document.text)

    seqchain_output["metadata"] = document.metadata
    return seqchain_output


def extract_documents(file_path):
    documents = get_origin_documents(file_path)
    all_documents = []
    for doc in documents:
        all_documents.append(write_overview_CV(doc, templates, llm, ovewview_template))
    return all_documents
