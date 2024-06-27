from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#modelo do gpt que será utilizado
modelo = "gpt-3.5-turbo"

def categoriza_jogo(nome_jogo, lista_categorias_possiveis):

    #instruções que devem ser seguidas pelo modelo
    prompt_sistema = f"""
            Você é um categorizador de jogos.
            Você deve assumir as categorias presentes na lista abaixo.

            # Lista de Categorias Válidas
            {lista_categorias_possiveis.split(",")}

            # Formato da Saída
            Produto: Nome do jogo
            Categoria: apresente a categoria do jogo

            # Exemplo de Saída
            Jogo: Diablo II
            Categoria: RPG
    """

    """
            "role":"system" -> Esta role é utilizada para definir o contexto ou as instruções que devem ser seguidas 
            pelo modelo de linguagem durante a conversa. Geralmente, é usada para fornecer informações sobre o 
            objetivo da interação, o tipo de resposta esperada, ou quaisquer outras diretrizes que o modelo deve seguir.
            
            "role" : "user" -> Esta role é utilizada para representar a entrada do usuário, ou seja, a pergunta, solicitação 
            ou informação que o usuário está enviando para o modelo de linguagem. É a parte da conversa que vem do 
            usuário, em oposição às instruções ou contexto fornecidos pelo "system".
            
            "model" -> qual modelo do gpt será utilizado para responder a pergunta do usuário   
            
            "temperature" -> grau de criatividade utilizado pelo bot
            
            "max_tokens" -> máximo de tokens da resposta
            
            "n" -> número de respostas criadas
    """  

    resposta = cliente.chat.completions.create(
        messages=[
            {
                "role":"system",
                "content": prompt_sistema
            },
            {
                "role":"user",
                "content": nome_jogo
            }
        ],
        model= modelo,
        temperature= 0,
        max_tokens= 50,
    )
    
    return resposta.choices[0].message.content


categorias_validas = ("Informe as categorias válidas, separadas por virgula: ")

while True:
    nome_jogo = input("Apresente o nome de um jogo: ")
    texto_resposta = categoriza_jogo(nome_jogo, categorias_validas)
    print(texto_resposta)
    
