from langchain.tools import tool
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from os import environ
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv('conf/.env')

model = ChatGoogleGenerativeAI(
    api_key = environ['GEMINI_API_KEY'],
    model="gemini-2.5-flash",
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=3000,
    timeout=10,
    # other params...
)

embeddings = GoogleGenerativeAIEmbeddings(
    api_key = environ['GEMINI_API_KEY'],
    model="models/gemini-embedding-001"
)

vector_store = Chroma(
    collection_name="transportation_bandung",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

vector_store_restaurant = Chroma(
    collection_name="rumah_makan_bandung",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

vector_store_rumah_sakit = Chroma(
    collection_name="rumah_sakit_bandung",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

# @tool
# def penjumlahan(a: int, b: int) -> int:
#     "fungsi untuk menjumlahkan 2 bilangan"
#     return a + b

# from langchain.tools import tool

@tool(response_format="content_and_artifact")
def retrieve_context_transportasi(query: str):
    """Mengambil informasi yang berhubungan dengan transportasi kota bandung"""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

@tool(response_format="content_and_artifact")
def retrieve_context_rumah_makan(query: str):
    """Mengambil informasi yang berhubungan tentang rumah makan/restoran di kota bandung"""
    retrieved_docs = vector_store_restaurant.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

@tool(response_format="content_and_artifact")
def retrieve_context_rumah_sakit(query: str):
    """Mengambil informasi yang berhubungan tentang rumah sakit di kota bandung"""
    retrieved_docs = vector_store_rumah_sakit.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs

def init_agent():
    system_prompt="""
    Kamu adalah pemandu cerdas yang mengetahui banyak hal soal kota Bandung. Gunakan tools berikut untuk menjawab pertanyaan
    1. `retrieve_context_rumah_makan` -> Pertanyaan terkait rumah makan
    2. `retrieve_context_transportasi` -> Pertanyaan terkait transportasi 
    3. `retrieve_context_rumah_sakit` -> Pertanyaan terkait rumah sakit 

    Selalu ingat aturan berikut
    1. SELALU menjawab pertanyaan berdasarkan tools
    2. JANGAN mengeluarkan pertanyaan di luar tools
    """
    agent = create_agent(
        model=model,
        tools=[retrieve_context_transportasi, retrieve_context_rumah_makan, retrieve_context_rumah_sakit],
        system_prompt=system_prompt,
    )
    return agent