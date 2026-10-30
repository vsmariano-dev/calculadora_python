# calculadora.py - Backend simples para as 4 operações

def calcular(num1, op, num2):
    # 1. Converte o texto recebido do HTML em número decimal
    try:
        n1 = float(num1)
        n2 = float(num2)
    except ValueError:
        return "Erro: Digite apenas números válidos!"

    # 2. As quatro operações básicas com if/elif/else
    if op == '+':
        return n1 + n2
    elif op == '-':
        return n1 - n2
    elif op == '*':
        return n1 * n2
    elif op == '/':
        # Proteção matemática essencial
        if n2 == 0:
            return "Erro: Não é possível dividir por zero!"
        return n1 / n2
    else:
        return "Erro: Operação inválida!"