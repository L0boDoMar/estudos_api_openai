from openai import OpenAI
import openai
from dotenv import load_dotenv  
import os  

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicia o cliente OpenAI e informa a chave de API a partir das variáveis de ambiente
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-3.5-turbo"  # Define o modelo a ser utilizado

# Função para carregar o conteúdo de um arquivo
def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo: 
            dados = arquivo.read()  
            return dados  
    except IOError as e:
        print(f"Erro: {e}")  # Exibe uma mensagem de erro caso ocorra um problema ao abrir o arquivo

# Função para salvar conteúdo em um arquivo
def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:  # Abre o arquivo no modo escrita com codificação UTF-8
            arquivo.write(conteudo)  # Escreve o conteúdo no arquivo
    except IOError as e:
        print(f"Não foi possivel salvar o arquivo {e}")  # Exibe uma mensagem de erro caso ocorra um problema ao salvar o arquivo
        
# Função para analisar sentimentos de avaliações de um jogo
def analisador_sentimentos(jogo):
    prompt_sistema = f"""
    Você é um analisador de sentimentos de avaliações de jogos.
    Escreva um parágrafo com até 50 palavras resumindo as avaliações e depois atribua qual o sentimento geral para o jogo analisado.
    Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

    # Formato de Saída

    Game:
    Resumo das Avaliações:
    Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
    Ponto fortes: lista com três bullets
    Pontos fracos: lista com três bullets
    """
    
    # Carrega o conteúdo das avaliações do jogo a partir de um arquivo
    prompt_usuario = carrega(f"./dados/avaliacoes/avaliacoes-{jogo}.txt")
    print(f"Iniciou a análise de sentimentos do jogo {jogo}")
    
    # Cria uma lista de mensagens para enviar para a API do OpenAI
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
    
    try:
        # Faz uma chamada para a API do OpenAI para gerar a resposta de análise de sentimentos
        resposta = cliente.chat.completions.create(
            messages = lista_mensagens,
            model = modelo
        )
        # Extrai o conteúdo da resposta da API
        texto_resposta = resposta.choices[0].message.content
        # Salva a resposta da análise de sentimentos em um arquivo
        salva(f"./dados/analise-{jogo}.txt", texto_resposta)
        print(f"Finalizou a análise de sentimentos do jogo {jogo}")
        
    except openai.AuthenticationError as e:
        print(f"Erro de autenticação: {e}")  # Exibe uma mensagem de erro caso ocorra um problema de autenticação
        
    except openai.APIError as e:
        print(f"Erro de API: {e}")  # Exibe uma mensagem de erro caso ocorra um problema na API

# Executa a função de análise de sentimentos para um determinado jogo
analisador_sentimentos("elden-ring")