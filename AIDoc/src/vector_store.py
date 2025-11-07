"""
Módulo para gerenciamento do vector store (FAISS)
"""
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def create_vector_store(chunks):
    """Cria um vector store usando FAISS e OpenAI Embeddings"""
    try:
        print("🔮 Criando índice inteligente...")
        print("⏳ Aguarde alguns minutos...")
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(chunks, embeddings)
        print("✅ Índice criado!")
        return vector_store
    except Exception as e:
        print(f"❌ Erro ao criar índice: {str(e)}")
        return None


def save_vector_store(vector_store, path="vectorstore"):
    """Salva o vector store em disco para reutilização"""
    try:
        vector_store.save_local(path)
        print("💾 Dados salvos para próxima vez")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar: {str(e)}")
        return False


def load_vector_store(path="../vectorstore"):
    """Carrega um vector store salvo anteriormente"""
    try:
        if not Path(path).exists():
            return None
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
        return vector_store
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {str(e)}")
        return None
