import typer
from loaders import load_pdf
from vectorstore import save_embeddings
from llm import main_chain

app = typer.Typer()

@app.command()
def load(file: str):
   """Este método insere todo o PDF na memória da IA"""
      
   file_to_embed = load_pdf(file)
   save_embeddings(file_to_embed)
   typer.echo('INFO - Arquivo corretamente carregado.')

@app.command()
def summarize(file: str):
   """Este método resume qualquer fonte de texto especificada"""
   ...

@app.command()
def ask(query: str):
   """Este método faz perguntas livres sobre qualquer PDF já carregado"""
   response = main_chain.invoke({"input": query})
   
   typer.echo(response["answer"])

if __name__ == "__main__":
   app()