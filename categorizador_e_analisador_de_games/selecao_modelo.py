from openai import OpenAI
import tiktoken
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4"

codificador = tiktoken.encoding_for_model(modelo)

def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")

prompt_sistema = """
Você é um categorizador de jogos.
Você deve assumir as categorias presentes na lista abaixo.

# Lista de Categorias Válidas: RPG, FPS, STEALTH, SURVIVAL HORROR, RTS, CORRIDA, ROGUE LIKE, LUTA, HACK AND SLASH

# Formato da Saída
Produto: Nome do jogo
Categoria: apresente a categoria do jogo

# Exemplo de Saída
Jogo: Diablo II
Categoria: RPG
"""

prompt_usuario = carrega("dados\Lista de games.txt")

lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario)
numero_de_tokens = len(lista_de_tokens)
print(f"Número de tokens na entrada: {numero_de_tokens}")
tamanho_esperado_saida = 2048

if numero_de_tokens >= 4096 - tamanho_esperado_saida:
    modelo = "gpt-4"
else:
    modelo = "gpt-3.5-turbo"

print(f"Modelo escolhido: {modelo}")

lista_mensagens = [
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": prompt_usuario
        }
    ]

resposta = client.chat.completions.create(
    messages = lista_mensagens,
    model=modelo
)

print(resposta.choices[0].message.content)