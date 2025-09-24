import typer
from loaders import load_pdf

app = typer.Typer()

@app.command()
def load(file: str):
   """Este método insere todo o PDF na memória da IA"""
      
   load_pdf(file)
   #TODO: Inserir na Vector Store

if __name__ == "__main__":
   app()