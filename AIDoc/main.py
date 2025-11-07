import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
import uvicorn


from src.rag_query import query_documents
from src.lanchain import initalize_langchain
from src.document_loader import load_documents_from_data, split_documents
from src.vector_store import create_vector_store, save_vector_store, load_vector_store
from src.interactive import test_rag_interactive
from pydantic import BaseModel



vector_store, llm = initalize_langchain()

app = FastAPI()


@app.get("/")
def initialize():
    return {
        "message": " ASSISTENTE INTELIGENTE DE DOCUMENTOS iniciado com sucesso!"
    }
class MessageRequest(BaseModel):
        message: str

@app.post("/msg")
def process_message(request: MessageRequest):
    message = request.message
    result = query_documents(vector_store, llm, message)
    return {"result": result['answer']}
    

if __name__ == "__main__":
    print(" ASSISTENTE INTELIGENTE DE DOCUMENTOS")
  
    uvicorn.run(app, host="0.0.0.0", port=8000)


