"""
Módulo de estudo interativo.
Aqui ficam as funções que conversam com o modelo de IA (via Ollama + LangChain).
"""

from typing import List
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

# Instância do modelo local
llm = OllamaLLM(model="llama2")

def gerar_resumo(texto: str) -> str:
    """
    Recebe um texto longo e gera um resumo organizado.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente que cria resumos claros e objetivos."),
        ("user", f"Resuma o seguinte texto em tópicos:\n\n{texto}")
    ])
    chain = prompt | llm
    return chain.invoke({})

def gerar_quiz(texto: str, num_perguntas: int = 5) -> List[str]:
    """
    Cria um quiz com base no texto. Retorna uma lista de perguntas.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um professor ajudando o aluno a estudar."),
        ("user", f"Crie {num_perguntas} perguntas de quiz sobre o seguinte texto:\n\n{texto}")
    ])
    chain = prompt | llm
    resposta = chain.invoke({})
    return [linha.strip() for linha in resposta.split("\n") if linha.strip()]

def responder_pergunta(pergunta: str, contexto: str) -> str:
    """
    O usuário faz uma pergunta. A IA responde com base em um contexto.
    (No futuro o contexto virá do vectorstore.py via FAISS).
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente de estudos."),
        ("user", f"Com base no seguinte contexto:\n\n{contexto}\n\nResponda: {pergunta}")
    ])
    chain = prompt | llm
    return chain.invoke({})
