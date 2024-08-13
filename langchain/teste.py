import os
from transformers import GPT2TokenizerFast
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from langchain.chains import ConversationalRetrievalChain
import textract

chave_openai = ""

doc = textract.process("dados/guerreiro.pdf")

with open('guerreiro.txt', 'w', encoding="utf-8") as f:
    f.write(doc.decode('utf-8'))

with open('guerreiro.txt', 'r', encoding="utf-8") as f:
    text = f.read()

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 512,
    chunk_overlap  = 24,
    length_function = count_tokens,
)

chunks = text_splitter.create_documents([text])
embeddings = OpenAIEmbeddings(openai_api_key=chave_openai, model="text-embedding-3-small")

db = FAISS.from_documents(chunks, embeddings)
query = "QUal é o principal atributo dos guerreiros?"
docs = db.similarity_search(query)
docs[0]

chain = load_qa_chain(OpenAI(openai_api_key=chave_openai, temperature=0), chain_type="stuff")

inputs = {
    "input_documents": docs,
    "question": query
}
response = chain.invoke(inputs)
print(response)
