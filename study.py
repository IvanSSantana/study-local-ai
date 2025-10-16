"""
Módulo de estudo interativo.
Aqui ficam as funções e nodes que conversam com o modelo de IA (via Ollama + LangChain + LangGraph).
"""

from llm import llm_study, screening, call_ai_RAG
from typing import List, TypedDict, Optional, Dict
from langchain.prompts import ChatPromptTemplate
import typer

class AgentState(TypedDict, total = False):
    user_message: str
    screening: Dict
    response: Optional[str]
    sucess_rag: bool
    final_action: str

def node_screening(state: AgentState) -> AgentState:
    typer.echo("Executando nó de triagem...")    

    user_message = state.get("user_message", "") # Pega o campo user_message e define vazio como valor padrão em caso de inexistência da chave no dicionário. Método do Python
    return {"screening": screening(user_message)}

def node_summarize(state: AgentState) -> AgentState:
    typer.echo("Executando nó de resumo...")

    user_message = state.get("user_message", "")
    response_rag = call_ai_RAG(user_message, "summarize")
    
    updated_state: AgentState = {
        "response": response_rag["answer"],
        "sucess_rag": response_rag["sucess_rag"]
    }

    if response_rag["sucess_rag"]:
        updated_state["final_action"] = "RESUMO"

    typer.echo("Nó de resumo concluído.")
    return updated_state

#TODO: Transformar todas funções abaixo em nodes.
def generate_quiz(text: str, num_questions: int = 5, essay: bool = False) -> List[str]:
    """
    Cria um quiz com base no texto. Retorna uma lista de perguntas. #TODO: Implementar mais tipos de questões (Ex: V ou F)
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente que cria perguntas objetivas ou dissertativas, sempre escolha SOMENTE UM TIPO DE QUESTÃO. Sempre haverá uma única alternativa correta para questões objetivas."),
        ("user", f"Crie {num_questions} perguntas de quiz sobre o seguinte texto:\n\n{text}. As questões são dissertativas: {essay}.")
    ])
    chain = prompt | llm_study
    response = chain.invoke({})
    typer.echo("Questões geradas com sucesso!")
    return [line.strip() for line in response.split("\n") if line.strip()]

def answer_asking(asking: str, context: str) -> str:
    """
    O usuário faz uma pergunta. A IA responde com base no contexto do PDF.
    (No futuro o contexto virá do 'vectorstore.py' via ChromaDB).
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente de estudos."),
        ("user", f"Com base no seguinte contexto:\n\n{context}\n\nResponda: {asking}")
    ])
    chain = prompt | llm_study
    typer.echo("Pergunta respondida com sucesso!")
    return chain.invoke({})
