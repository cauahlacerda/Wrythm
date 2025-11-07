"""
Módulo para carregamento e processamento de documentos PDF
"""
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents_from_data():
    """Carrega todos os documentos PDF da pasta data"""
    try:
        data_path = Path("data")
        if not data_path.exists():
            print("❌ Pasta 'data' não encontrada!")
            return None
        
        print(f"📁 Lendo documentos...")
        pdf_files = list(data_path.glob("*.pdf"))
        
        if not pdf_files:
            print("⚠️ Nenhum PDF encontrado na pasta 'data'")
            return None
        
        all_documents = []
        
        for pdf_file in pdf_files:
            try:
                loader = PyPDFLoader(str(pdf_file))
                documents = loader.load()
                all_documents.extend(documents)
            except Exception as e:
                print(f"   ⚠️ Não foi possível ler {pdf_file.name}")
        
        print(f"✅ {len(all_documents)} páginas carregadas")
        return all_documents
    except Exception as e:
        print(f"❌ Erro ao carregar documentos: {str(e)}")
        return None


def split_documents(documents):
    """Divide os documentos em chunks menores para processamento"""
    try:
        print("✂️ Organizando informações...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_documents(documents)
        return chunks
    except Exception as e:
        print(f"❌ Erro ao processar: {str(e)}")
        return None
