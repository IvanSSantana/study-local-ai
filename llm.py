from langchain.chains import create_retrieval_chain
from langchain_ollama import OllamaLLM
from pydantic import BaseModel
from typing import Literal, Dict
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from vectorstore import load_vectorstore
from langchain.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough

# CONFIGURANDO MODELO DE RESUMO
    
# Modelo rápido com menos criatividade 
llm_study = OllamaLLM (
    model="smollm:135m",
    temperature=0.3
)

vectorstore, retriever = load_vectorstore()

SCREENING_PROMPT = (
    "Você é um triador de estudos gerais para arquivos que lhe forem fornecidos. "
    "Dada a mensagem do usuário, retorne SOMENTE um JSON com:\n"
    "{\n"
    '  "decision": "RESUMO" | "FLASHCARD" | "QUESTÕES" | "LIVRE",\n'
    "}\n"
    "Regras:\n"
    '- **RESUMO**: Pedidos de resumo, simplificação ou encurtamento de textos (Ex: "Resuma o livro fornecido sobre a Independência do Brasil.").\n'
    '- **FLASHCARD**: Pedidos de criação de flashcards, cartão de memorização ou cartões Anki (Ex: "Faça um cartão de memorização sobre colcheias pontuadas conforme o arquivo fornecido.").\n'
    '- **QUESTÕES**: Solicitações para fazer lista de questões, exercícios, provas, testes ou correlatos (Ex: "Elabore para mim um teste com base no arquivo fornecido.").\n'
    '- **LIVRE**: Perguntas acerca de informações específicas dentro dos arquivos (Ex: "Qual o nome de meu novo projeto conforme o arquivo?", "Qual o assunto principal do último PDF fornecido?").'
    "Analise a mensagem e decida a ação mais apropriada."
)

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

prompt_rag = ChatPromptTemplate.from_messages([
    ("system",
     "Você é um assistente de estudos pessoais sobre qualquer tema."
     "Responda SOMENTE com base no contexto fornecido."
     "As perguntas podem se referir de forma indireta, na terceira pessoa ou do ponto de vista delas sobre os PDFs, cabe você interpretar corretamente."
     "Se não houver base suficiente, responda apenas 'Não tenho informações suficientes para uma resposta adequada.'."),

    ("human", "Pergunta: {input}\n\nContexto:\n{context}")
])

docs_chain = create_stuff_documents_chain(llm=llm_screening, prompt=prompt_rag)

main_chain = create_retrieval_chain(vectorstore.as_retriever(), docs_chain)

#TODO: Configurar corretamente LLM + Retriever para nodes