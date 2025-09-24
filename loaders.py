import pdfplumber

def load_pdf(file_dir: str) -> str:

    with pdfplumber.open(file_dir) as pdf:
        pdf_text: str = ""

        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text: # Verifica se há texto na página para evitar adicionar linhas vazias
                pdf_text += page_text + "\n" # Adiciona quebra de linha entre as páginas

    return pdf_text