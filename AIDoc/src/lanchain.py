
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv


from src.document_loader import load_documents_from_data, split_documents
from src.vector_store import create_vector_store, load_vector_store, save_vector_store, save_vector_store

load_dotenv()

def initalize_langchain():
    """Função principal que coordena o processo RAG"""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print(" Chave da OpenAI não encontrada!")
            print(" Configure o arquivo .env com sua chave API")
            return False
        
        print(" Conectado!")
        print(" Inicializando assistente...")
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        
        vector_store = load_vector_store()
        if vector_store:
            print(" Documentos carregados da memória")
        else:
            print("\n Primeira execução - processando documentos...")
            documents = load_documents_from_data()
            if not documents:
                print("\n Nenhum documento encontrado na pasta 'data'")
                return False
            chunks = split_documents(documents)
            if not chunks:
                print("\n Erro ao processar documentos")
                return False
            print(f"\n Processados: {len(documents)} páginas em {len(chunks)} partes")
            vector_store = create_vector_store(chunks)
            if not vector_store:
                print("\n Erro ao criar índice de busca")
                return False
            save_vector_store(vector_store)
        
        # Inicia modo interativo
        # test_rag_interactive(vector_store, llm)
        
        return vector_store,llm
    except Exception as e:
        print(f"\n Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
