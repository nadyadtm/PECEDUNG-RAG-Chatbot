from dotenv import load_dotenv
from os import environ
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv('conf/.env')

embeddings = GoogleGenerativeAIEmbeddings(
    api_key = environ['GEMINI_API_KEY'],
    model="models/gemini-embedding-001"
)

def store_vector_restaurant():
    print("Mulai Menyimpan...")
    vector_store_restaurant = Chroma(
        collection_name="tempat_makan_bandung",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
    )
    classs = "clearfix"

    # Only keep post title, headers, and content from the full HTML.
    bs4_strainer = bs4.SoupStrainer(class_=(classs))
    loader = WebBaseLoader(
        web_paths=("https://www.kompas.com/food/read/2023/09/02/131700875/35-tempat-makan-enak-di-bandung-dari-legendaris-hingga-kekinian?page=all",),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # chunk size (characters)
        chunk_overlap=200,  # chunk overlap (characters)
        add_start_index=True,  # track index in original document
    )
    all_splits = text_splitter.split_documents(docs)
    document_ids = vector_store_restaurant.add_documents(documents=all_splits)

    print("Selesai Menyimpan Vector Store Tema Restaurant di Bandung")

def store_vector_transport():
    print("Mulai Menyimpan...")
    vector_store_restaurant = Chroma(
        collection_name="transportation_bandung",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
    )

    bs4_strainer = bs4.SoupStrainer(class_=("centered-content"))
    loader = WebBaseLoader(
        web_paths=("https://transportforbandung.org/peta/bus-kota",),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # chunk size (characters)
        chunk_overlap=200,  # chunk overlap (characters)
        add_start_index=True,  # track index in original document
    )
    all_splits = text_splitter.split_documents(docs)
    document_ids = vector_store_restaurant.add_documents(documents=all_splits)

    print("Selesai Menyimpan Vector Store Tema Transportasi di Bandung")

def store_vector_rumah_sakit():
    print("Mulai Menyimpan...")
    vector_store_rumah_sakit = Chroma(
        collection_name="rumah_sakit_bandung",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
    )

    classs = "long-description__wrapper"

    # Only keep post title, headers, and content from the full HTML.
    bs4_strainer = bs4.SoupStrainer(class_=(classs))
    loader = WebBaseLoader(
        web_paths=("https://www.rumah123.com/explore/kota-bandung/rumah-sakit-di-bandung/",),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # chunk size (characters)
        chunk_overlap=200,  # chunk overlap (characters)
        add_start_index=True,  # track index in original document
    )
    all_splits = text_splitter.split_documents(docs)
    document_ids = vector_store_rumah_sakit.add_documents(documents=all_splits)

    print("Selesai Menyimpan Vector Store Tema Rumah Sakit di Bandung")

def main():
    store_vector_restaurant()
    store_vector_transport()
    store_vector_rumah_sakit()

if __name__ == "__main__":
    main()
