import pdfplumber
import typer
from langchain.schema import Document
from typing import List

def load_pdf(file_dir: str) -> List[Document]:

    try:
        with pdfplumber.open(file_dir) as pdf:
            doc = []

            for page_number, page in enumerate(pdf.pages):
                page_text = page.extract_text()

                if page_text: # Verifica se há texto na página para evitar adicionar linhas vazias
                    doc.append(Document(page_content=page_text, metadata={"page": page_number+1}))

        typer.echo("INFO - Arquivo lido com sucesso.")
        return doc
    except:
        raise Exception("ERROR - Ocorreu um erro durante a leitura do PDF")
        