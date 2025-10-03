"""
Script simples para testar as funções do study.py
"""

from study import generate_summarize, generate_quiz, answer_asking
import pytest

# Texto de exemplo para os testes
texto = """
A fotossíntese é um processo biológico realizado por plantas, algas e algumas bactérias.
Nesse processo, a energia da luz solar é usada para converter dióxido de carbono e água
em glicose e oxigênio. Esse processo é fundamental para a vida na Terra, pois fornece o
oxigênio que respiramos e a base da cadeia alimentar.
"""

def test_summarize(capsys):
    print("\n=== TESTE RESUMO ===")
    resumo = generate_summarize(texto)
    print(resumo)

    output = capsys.readouterr()
    assert "Resumo gerado com sucesso!" in output.out

def test_quiz(capsys):
    print("\n=== TESTE QUIZ ===")
    quiz = generate_quiz(texto, num_perguntas=3)
    for i, pergunta in enumerate(quiz, 1):
        print(f"{i}. {pergunta}")

    output = capsys.readouterr()
    assert "Questões geradas com sucesso!" in output.out

def test_asking(capsys):
    print("\n=== TESTE PERGUNTA LIVRE ===")
    resposta = answer_asking("Qual é a importância da fotossíntese?", texto)
    print(resposta)

    output = capsys.readouterr()
    assert "Pergunta respondida com sucesso!" in output.out
