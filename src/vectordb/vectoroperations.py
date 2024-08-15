# app/services/vector_operations.py

import logging
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import lancedb
import os
import sqlite3

logger = logging.getLogger(__name__)

LANCEDB_PATH = os.path.join(os.getcwd(), "data", "lancedb")

class VectorOperations:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()

    def get_db_connection(self):
        os.makedirs(LANCEDB_PATH, exist_ok=True)
        return lancedb.connect(LANCEDB_PATH)

    def load_and_split_documents(self, file_paths: List[str]):
        logger.info(f"Loading documents from: {file_paths}")
        all_splits = []
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=200)
        for file_path in file_paths:
            loader = PyMuPDFLoader(file_path)
            documents = loader.load()
            splits = text_splitter.split_documents(documents)
            all_splits.extend(splits)
        logger.info(f"Documents split into {len(all_splits)} chunks")
        return all_splits

    def create_vectorstore(self, splits, table_name):
        logger.info("Creating vector store")
        db = self.get_db_connection()
        
        data = [{
            "id": str(i),
            "text": doc.page_content,
            "vector": self.embeddings.embed_query(doc.page_content),
            "metadata": doc.metadata
        } for i, doc in enumerate(splits)]
        
        table = db.create_table(table_name, data=data, mode="overwrite")
        logger.info("Vector store created successfully")
        return table

    def search_documents(self, table_name: str, query: str, k: int = 4):
        db = self.get_db_connection()
        table = db.open_table(table_name)
        query_vector = self.embeddings.embed_query(query)
        results = table.search(query_vector).limit(k).to_pandas()
        return results


