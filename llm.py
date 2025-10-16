from langchain.chains import create_retrieval_chain
from langchain_ollama import OllamaLLM
from pydantic import BaseModel
from typing import Literal, Dict
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from vectorstore import load_vectorstore
from langchain.output_parsers import PydanticOutputParser
import json

# CONFIGURANDO MODELO DE RESUMO

# Modelo rápido com menos criatividade 
llm_study = OllamaLLM (
    model="smollm:135m",
    temperature=0.3
)

vectorstore, retriever = load_vectorstore()

with open(f"prompts_config.json", encoding="utf8") as json_file:
        data = json.load(json_file)

        SCREENING_PROMPT = data["screening"]["system"]

class ScreeningOut(BaseModel):
    decision: Literal["RESUMO", "FLASHCARD", "QUESTÕES", "LIVRE"]

llm_screening = OllamaLLM (
    model="smollm:135m",
    temperature=0.1
)

parser = PydanticOutputParser(pydantic_object=ScreeningOut)

def screening(message: str) -> Dict:
    output = llm_screening.invoke([
        SystemMessage(content=SCREENING_PROMPT), # Prompt de configuração
        HumanMessage(content=message)
])

    structured_output = parser.parse(output.text) # type: ignore

    return structured_output  # type: ignore

def invoke_llm(prompt_name: str):
    with open(f"prompts_config.json", encoding="utf8") as json_file:
        data = json.load(json_file)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", data[prompt_name]["system"]),
        ("user", data[prompt_name]["user"])
    ])

    docs_chain = create_stuff_documents_chain(llm=llm_study, prompt=prompt)

    chain = create_retrieval_chain(vectorstore.as_retriever(), docs_chain)
    
    return chain

def call_ai_RAG(asking: str, prompt_name: str = "free"):
    associated_docs = retriever.get_relevant_documents(asking)

    if not associated_docs:
        return {
        "answer": "Não tenho informações suficientes para uma resposta adequada.",
        "sucess_rag": False
        }

    chain = invoke_llm(prompt_name)

    answer: str = chain.invoke({"input": asking, "context": associated_docs}).strip() or ""

    if answer == "Não tenho informações suficientes para uma resposta adequada.":
        return {
            "answer": answer,
            "sucess_rag": False 
        }

    return {
        "answer": answer,
        "sucess_rag": True
    }
