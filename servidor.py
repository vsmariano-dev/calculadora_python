"""
servidor.py - Servidor Web minimalista em Python puro.
NÃO CONTÉM CÓDIGO HTML DENTRO DO PYTHON!
Lê os arquivos 'formulario.html' e 'resultado.html' diretamente do disco.

Como rodar no seu computador:
1. python3 servidor.py
2. Abra no navegador: http://localhost:3000
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
import sys
from calculadora import calcular

PORT = 3000
if "--port" in sys.argv:
    try:
        idx = sys.argv.index("--port")
        PORT = int(sys.argv[idx + 1])
    except (IndexError, ValueError):
        pass
elif "PORT" in os.environ:
    PORT = int(os.environ["PORT"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class ServidorCalculadora(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

    def do_GET(self):
        # 1. Lê a página de formulário HTML do arquivo externo formulario.html
        caminho_form = os.path.join(BASE_DIR, "formulario.html")
        try:
            with open(caminho_form, "r", encoding="utf-8") as f:
                conteudo_html = f.read()
            status = 200
        except FileNotFoundError:
            conteudo_html = "<h1>Arquivo formulario.html não encontrado!</h1>"
            status = 404

        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(conteudo_html.encode("utf-8"))

    def do_POST(self):
        # 2. Recebe os dados enviados pelo formulário HTML
        tamanho = int(self.headers.get("Content-Length", 0))
        dados_recebidos = self.rfile.read(tamanho).decode("utf-8")
        parametros = urllib.parse.parse_qs(dados_recebidos)

        num1 = parametros.get("num1", ["0"])[0]
        op = parametros.get("op", ["+"])[0]
        num2 = parametros.get("num2", ["0"])[0]

        # 3. Executa a função Python pura em calculadora.py
        resposta = calcular(num1, op, num2)

        # 4. Lê o arquivo externo resultado.html (Nenhum HTML hardcoded aqui!)
        caminho_res = os.path.join(BASE_DIR, "resultado.html")
        try:
            with open(caminho_res, "r", encoding="utf-8") as f:
                template_resultado = f.read()
            status = 200
        except FileNotFoundError:
            template_resultado = "<h1>Arquivo resultado.html não encontrado!</h1>"
            status = 404

        if resposta["sucesso"]:
            valor_resultado = str(resposta["resultado"])
            texto_expressao = resposta["expressao"]
            classe_erro = ""
        else:
            valor_resultado = "Erro"
            texto_expressao = resposta["erro"]
            classe_erro = " erro"

        # 5. Preenche os marcadores no arquivo resultado.html
        pagina_final = template_resultado.replace("{resultado}", valor_resultado)
        pagina_final = pagina_final.replace("{expressao}", texto_expressao)
        if classe_erro:
            pagina_final = pagina_final.replace('class="resultado"', 'class="resultado erro"')

        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(pagina_final.encode("utf-8"))

def iniciar_servidor(porta=PORT):
    servidor = HTTPServer(("0.0.0.0", porta), ServidorCalculadora)
    print(f"Servidor Python rodando em http://localhost:{porta}")
    print("Código HTML 100% isolado nos arquivos 'formulario.html' e 'resultado.html'.")
    servidor.serve_forever()

if __name__ == "__main__":
    iniciar_servidor()
