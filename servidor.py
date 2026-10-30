# servidor.py - Servidor Web nativo do Python (execute: python3 servidor.py)
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from calculadora import calcular

class ServidorCalculadora(BaseHTTPRequestHandler):
    def do_GET(self):
        # Entrega a página HTML simples
        with open("index.html", "r", encoding="utf-8") as f:
            pagina = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(pagina.encode("utf-8"))

    def do_POST(self):
        # Lê os dados enviados pelo formulário HTML
        tamanho = int(self.headers.get("Content-Length", 0))
        dados_brutos = self.rfile.read(tamanho).decode("utf-8")
        campos = urllib.parse.parse_qs(dados_brutos)

        n1 = campos.get("num1", ["0"])[0]
        op = campos.get("op", ["+"])[0]
        n2 = campos.get("num2", ["0"])[0]

        # Executa o cálculo no Python
        resultado = calcular(n1, op, n2)

        # Retorna a resposta para a tela
        resposta_html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <body style="font-family: sans-serif; max-width: 360px; margin: 50px auto; text-align: center;">
            <h2>Resultado: {n1} {op} {n2} = {resultado}</h2>
            <br>
            <a href="/" style="display: inline-block; padding: 10px 20px; background: #0284c7; color: white; text-decoration: none; border-radius: 4px;">Fazer Outro Cálculo</a>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(resposta_html.encode("utf-8"))

print("Servidor Python rodando em http://localhost:8000")
HTTPServer(("0.0.0.0", 8000), ServidorCalculadora).serve_forever()