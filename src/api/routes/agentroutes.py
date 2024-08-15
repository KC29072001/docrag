import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import uuid
import shutil
from src.vectordb.vectoroperations import VectorOperations
from datetime import datetime
import asyncio 
import sqlite3


logger = logging.getLogger(__name__)

router = APIRouter()

vector_ops = VectorOperations()


class DocumentLoadRequest(BaseModel):
    file_paths: List[str]
    user_id: Optional[str] = None


class ChatMessage(BaseModel):
    chat_thread_id: str
    message: str

class ChatStart(BaseModel):
    asset_id: str




@router.post("/documents/process")
async def process_documents(request: DocumentLoadRequest):
    try:
        if not request.file_paths:
            raise ValueError("No file paths provided")

        asset_ids = {}
        for file_path in request.file_paths:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Generate a unique assetID for each file
            asset_id = str(uuid.uuid4())
            asset_ids[file_path] = asset_id

        logger.info(f"Received request to load documents: {request.file_paths}")

        # Load and split documents
        splits = vector_ops.load_and_split_documents(request.file_paths)
        logger.info(f"Documents split into {len(splits)} chunks")
        
        table_name = f"user_{asset_id}_embeddings"
        vector_ops.create_vectorstore(splits, table_name)
        logger.info("Vector store created")

        return {"message": "Documents processed successfully", "files_loaded": request.file_paths, "asset_id": asset_id}
    except Exception as e:
        logger.exception("An error occurred while loading documents")
        raise HTTPException(status_code=500, detail=str(e))


    


def check_document_exists(asset_id: str) -> bool:
    file_path = f"data/lancedb/user_{asset_id}_embeddings.lance"
    return os.path.exists(file_path)

def associate_thread_with_asset(chat_thread_id: str, asset_id: str):
    conn = sqlite3.connect('chat_threads.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_threads
        (chat_thread_id TEXT PRIMARY KEY, asset_id TEXT)
    ''')
    
    # Insert the association
    cursor.execute('''
        INSERT INTO chat_threads (chat_thread_id, asset_id)
        VALUES (?, ?)
    ''', (chat_thread_id, asset_id))
    
    conn.commit()
    conn.close()




@router.post("/chat/start")
async def start_chat(chat_start: ChatStart):
    try:
        asset_id = chat_start.asset_id
        
        # Check if the asset_id exists
        if not check_document_exists(asset_id):
            raise HTTPException(status_code=404, detail=f"Asset with ID {asset_id} not found")
        
        # Generate a new chat_thread_id
        chat_thread_id = str(uuid.uuid4())
        
        # Associate the chat_thread_id with the asset_id
        associate_thread_with_asset(chat_thread_id, asset_id)
        
        logger.info(f"Started new chat thread {chat_thread_id} for asset {asset_id}")
        
        return {"chat_thread_id": chat_thread_id}
    
    except Exception as e:
        logger.exception("An error occurred while starting a new chat")
        raise HTTPException(status_code=500, detail=str(e))



def get_asset_id_from_thread(chat_thread_id: str) -> str:
    conn = sqlite3.connect('chat_threads.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT asset_id FROM chat_threads WHERE chat_thread_id = ?', (chat_thread_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result is None:
        raise HTTPException(status_code=404, detail=f"Chat thread with ID {chat_thread_id} not found")
    
    return result[0]



@router.post("/chat/message")
async def chat(request: ChatMessage):
    try:
        chat_thread_id = request.chat_thread_id
        
        # Get the asset_id associated with this chat_thread_id
        asset_id = get_asset_id_from_thread(chat_thread_id)
        
        # Check if the document exists
        if not check_document_exists(asset_id):
            raise HTTPException(status_code=400, detail="Documents not loaded for this asset. Please load documents first.")
        
        table_name = f"user_{asset_id}_embeddings"
        file_path = f"data/lancedb/{table_name}.lance"
        
        logger.info(f"Received chat message from thread {chat_thread_id}: {request.message}")
        
        # Connect to the LanceDB table
        db = vector_ops.get_db_connection()
        if table_name not in db.table_names():
            raise HTTPException(status_code=400, detail="Documents not loaded for this user. Please load documents first.")
        
        logger.info(f"Received chat message from thread {chat_thread_id}: {request.message}")
        
        results = vector_ops.search_documents(table_name, request.message)
        
        response = results.iloc[0]['text'] if not results.empty else "No relevant information found."
        
        logger.info(f"Generated response for thread {chat_thread_id}: {response}")
        
        return {"response": response}
    except Exception as e:
        logger.exception("An error occurred during chat")
        raise HTTPException(status_code=500, detail=str(e))