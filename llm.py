from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Ollama

# CONFIGURANDO MODELO DE RESUMO

# Modelo rápido com menos criatividade 
llm_summarize = Ollama (
    model="gemma3:270m",
    temperature=0.3
)

# Configuração do resumo
summarize_prompt = PromptTemplate.from_template("""
    Gsere SOMENTE um resumo do eguinte texto: {text} 
""")

chain = LLMChain(llm=llm_summarize, prompt=summarize_prompt)

