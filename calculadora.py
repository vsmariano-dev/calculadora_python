"""
calculadora.py - Backend simples em Python para as 4 operações básicas.
Recebe os valores, calcula e retorna o resultado em formato JSON.
"""
import sys
import json

def calcular(num1, op, num2):
    # 1. Validação simples dos números
    try:
        n1 = float(num1)
        n2 = float(num2)
    except (ValueError, TypeError):
        return {
            "sucesso": False,
            "erro": "Por favor, digite números válidos."
        }

    # 2. As quatro operações básicas da forma mais simples
    if op == "+":
        resultado = n1 + n2
    elif op == "-":
        resultado = n1 - n2
    elif op == "*":
        resultado = n1 * n2
    elif op == "/":
        # Proteção matemática: divisão por zero
        if n2 == 0:
            return {
                "sucesso": False,
                "erro": "Erro: Não é possível dividir por zero!"
            }
        resultado = n1 / n2
    else:
        return {
            "sucesso": False,
            "erro": f"Operação '{op}' inválida! Escolha +, -, * ou /."
        }

    # Se for inteiro (ex: 4.0), podemos formatar de forma limpa
    formatado = int(resultado) if resultado.is_integer() else round(resultado, 4)
    n1_fmt = int(n1) if n1.is_integer() else n1
    n2_fmt = int(n2) if n2.is_integer() else n2

    return {
        "sucesso": True,
        "num1": n1_fmt,
        "operacao": op,
        "num2": n2_fmt,
        "resultado": formatado,
        "expressao": f"{n1_fmt} {op} {n2_fmt} = {formatado}"
    }

if __name__ == "__main__":
    # Permite ser chamado pelo terminal ou pelo backend web:
    # Exemplo: python3 calculadora.py 10 + 5
    if len(sys.argv) >= 4:
        num1 = sys.argv[1]
        operacao = sys.argv[2]
        num2 = sys.argv[3]
        resposta = calcular(num1, operacao, num2)
        print(json.dumps(resposta, ensure_ascii=False))
    else:
        print(json.dumps({
            "sucesso": False,
            "erro": "Uso: python3 calculadora.py <num1> <operacao> <num2>"
        }, ensure_ascii=False))
