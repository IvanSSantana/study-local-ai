from study_local_ai.loaders import load_pdf
import pytest
import os

# Obtém o caminho absoluto para o diretório onde o teste está localizado
TEST_DIR = os.path.dirname(os.path.abspath(__file__))

def test_load_sucess(capsys):
   """
    Testa o carregamento bem-sucedido de um arquivo PDF.
    O caminho para o arquivo de teste é construído dinamicamente
    para garantir que o teste funcione de qualquer diretório.
    """
   
   pdf_path = os.path.join(TEST_DIR, 'short_pdf_test.pdf')
   load_pdf(pdf_path)

   output = capsys.readouterr()
   assert "INFO - Arquivo lido com sucesso." in output.out

def test_load_error(capsys):
   with pytest.raises(Exception, match="ERROR - Ocorreu um erro durante a leitura do PDF"):
      load_pdf('error_file.pdf')