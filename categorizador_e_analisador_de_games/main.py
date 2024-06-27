from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Inicia o cliente OpenAI e informa a chave de api
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


        # "role":"system" -> Esta role é utilizada para definir o contexto ou as instruções que devem ser seguidas 
        # pelo modelo de linguagem durante a conversa. Geralmente, é usada para fornecer informações sobre o 
        # objetivo da interação, o tipo de resposta esperada, ou quaisquer outras diretrizes que o modelo deve seguir.
        
        # "role" : "user" -> Esta role é utilizada para representar a entrada do usuário, ou seja, a pergunta, solicitação 
        # ou informação que o usuário está enviando para o modelo de linguagem. É a parte da conversa que vem do 
        # usuário, em oposição às instruções ou contexto fornecidos pelo "system".
        
        # "model" -> qual modelod o gpt será utilizado para responder a pergunta do usuário   
 
resposta = cliente.chat.completions.create(
    messages=[
        {
            "role":"system",
            "content":"Listar apenas os nomes dos jogos, sem considerar descrição."
        },
        {
            "role":"user",
            "content":"Recomende 3 jogos"
        }
    ],
    model="gpt-3.5-turbo"
)

print(resposta.choices[0].message.content)
