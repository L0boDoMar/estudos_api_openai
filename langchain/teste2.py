import os
from transformers import GPT2TokenizerFast
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import textract

# Chave da API OpenAI
chave_openai = ""

# Processa o arquivo PDF para extrair o texto
doc = textract.process("dados/guerreiro.pdf")
with open('guerreiro.txt', 'w', encoding="utf-8") as f:
    f.write(doc.decode('utf-8'))

# Lê o texto extraído do arquivo
with open('guerreiro.txt', 'r', encoding="utf-8") as f:
    text = f.read()

# Inicializa o tokenizador GPT-2 para contagem de tokens
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

# Função para contar tokens no texto
def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

# Inicializa o divisor de texto para dividir o texto em pedaços menores
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 512,  # Tamanho máximo de cada pedaço
    chunk_overlap  = 24,  # Sobreposição entre pedaços
    length_function = count_tokens,  # Função para contar tokens
)

# Cria pedaços de texto e inicializa o índice FAISS
chunks = text_splitter.create_documents([text])
embeddings = OpenAIEmbeddings(openai_api_key=chave_openai, model="text-embedding-3-small")
db = FAISS.from_documents(chunks, embeddings)

# Inicializa o modelo OpenAI
llm = OpenAI(openai_api_key=chave_openai, temperature=0)

# Cria o PromptTemplate para o sistema de QA
qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        ("human", "{input}"),
    ]
)

# Cria a cadeia de perguntas e respostas
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# Cria o recuperador de histórico
history_aware_retriever = db.as_retriever()

# Cria a cadeia de recuperação com histórico
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# Histórico da conversa para manter o contexto
chat_history = []

def ask_question(question: str):
    global chat_history
    inputs = {
        "input": question,
        "chat_history": chat_history
    }
    
    print(f"Inputs antes da consulta: {inputs}")  # Adiciona log dos inputs
    
    # Faz a consulta à cadeia de recuperação com histórico
    try:
        response = rag_chain.invoke(inputs)
    except Exception as e:
        print(f"Erro ao invocar a cadeia: {e}")  # Adiciona log de erro
        return "Ocorreu um erro ao processar a pergunta."
    
    # Adiciona a pergunta e a resposta ao histórico
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=response["answer"]))
    
    print(f"Resposta: {response['answer']}")  # Adiciona log da resposta
    print(f"Histórico atualizado: {chat_history}")  # Adiciona log do histórico atualizado
    
    return response["answer"]

# Teste: Exemplo de como fazer uma pergunta
query = "Qual é o principal atributo dos guerreiros?"  # Pergunta de teste
response = ask_question(query)
print("Resposta final:", response)

# Adicionando mais perguntas para testar o contexto
query2 = "Quais são os dados de vida dos guerreiros?"
response2 = ask_question(query2)
print("Resposta 2:", response2)

query3 = "De quem estamos falando?"
response3 = ask_question(query3)
print("Resposta 3:", response3)
