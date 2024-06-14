import os
from dotenv import load_dotenv

import openai
import shutil

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

openai.api_key = os.environ['OPENAI_API_KEY']

def main():
    generate_db()

def generate_db():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_db(chunks)

def load_documents():
    loader = DirectoryLoader("data", glob="*md")
    documents = loader.load()
    return documents


def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100,
        length_function = len,
        add_start_index = True,
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[30]
    print(document.page_content)
    print(document.metadata)

    return chunks

CHROMA_PATH = "chroma"

def save_to_db(chunks):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory = CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()

