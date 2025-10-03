"""
study.py
Módulo de estudo interativo.
Aqui ficam as funções que conversam com o modelo de IA (via Ollama + LangChain).
"""

from typing import List
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import typer

# Instância do modelo local
llm = OllamaLLM(model="llama2")

def generate_summarize(text: str) -> str:
    """
    Recebe um texto longo e gera um resumo organizado.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente que cria resumos claros e objetivos."),
        ("user", f"Resuma o seguinte texto em tópicos:\n\n{text}")
    ])
    chain = prompt | llm
    typer.echo("Resumo gerado com sucesso!")
    return chain.invoke({})

def generate_quiz(text: str, num_questions: int = 5, essay: bool = False) -> List[str]:
    """
    Cria um quiz com base no texto. Retorna uma lista de perguntas. #TODO: Implementar mais tipos de questões (Ex: V ou F)
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente que cria perguntas objetivas ou dissertativas, sempre escolha SOMENTE UM TIPO DE QUESTÃO. Sempre haverá uma única alternativa correta para questões objetivas."),
        ("user", f"Crie {num_questions} perguntas de quiz sobre o seguinte texto:\n\n{text}. As questões são dissertativas: {essay}.")
    ])
    chain = prompt | llm
    response = chain.invoke({})
    typer.echo("Questões geradas com sucesso!")
    return [line.strip() for line in response.split("\n") if line.strip()]

def answer_asking(asking: str, context: str) -> str:
    """
    O usuário faz uma pergunta. A IA responde com base no contexto do PDF.
    (No futuro o contexto virá do 'vectorstore.py' via ChromeDB).
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente de estudos."),
        ("user", f"Com base no seguinte contexto:\n\n{context}\n\nResponda: {asking}")
    ])
    chain = prompt | llm
    typer.echo("Pergunta respondida com sucesso!")
    return chain.invoke({})
