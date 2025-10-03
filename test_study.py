"""
test_study.py
Script simples para testar as funções do study.py
"""

from study import gerar_resumo, gerar_quiz, responder_pergunta

# Texto de exemplo para os testes
texto = """
A fotossíntese é um processo biológico realizado por plantas, algas e algumas bactérias.
Nesse processo, a energia da luz solar é usada para converter dióxido de carbono e água
em glicose e oxigênio. Esse processo é fundamental para a vida na Terra, pois fornece o
oxigênio que respiramos e a base da cadeia alimentar.
"""

def testar_resumo():
    print("\n=== TESTE RESUMO ===")
    resumo = gerar_resumo(texto)
    print(resumo)

def testar_quiz():
    print("\n=== TESTE QUIZ ===")
    quiz = gerar_quiz(texto, num_perguntas=3)
    for i, pergunta in enumerate(quiz, 1):
        print(f"{i}. {pergunta}")

def testar_pergunta():
    print("\n=== TESTE PERGUNTA LIVRE ===")
    resposta = responder_pergunta("Qual é a importância da fotossíntese?", texto)
    print(resposta)

if __name__ == "__main__":
    testar_resumo()
    testar_quiz()
    testar_pergunta()
