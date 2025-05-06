from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import chromadb

client = chromadb.PersistentClient(path="db")
# Загрузка данных из CSV (пример структуры: question,answer)
loader = CSVLoader("data.csv")
documents = loader.load()

# Разбивка на чанки
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Создание векторной БД
embeddings = OllamaEmbeddings(model="llama3", base_url="http://localhost:11434")
vector_db = Chroma.from_documents(
    client=client,
    documents=texts,
    embedding=embeddings,
    collection_name="faq_collection"
)