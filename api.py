from fastapi import FastAPI
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain_ollama import OllamaLLM

app = FastAPI()

# Инициализация компонентов
embeddings = OllamaEmbeddings(model="llama3")
vector_db = Chroma(persist_directory="db", embedding_function=embeddings)
llm = OllamaLLM(model="llama3", base_url="http://localhost:11434")

qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    retriever=vector_db.as_retriever(),
    chain_type="stuff",
    input_key="question"
)

class Query(BaseModel):
    question: str
@app.get("/")
async def home():
    return {"status": "API работает"}

@app.post("/ask")
async def ask_question(query: Query):
    response = qa_chain.invoke({"query": query.question})
    return {"answer": response["result"]}