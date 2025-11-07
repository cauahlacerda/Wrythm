import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

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

def load_vector_store(path="vectorstore"):
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

def query_documents(vector_store, llm, question):
    """
    Função RAG que processa uma pergunta e retorna resposta baseada nos documentos.
    Esta função será usada pela rota da API.
    
    Args:
        vector_store: O FAISS vector store com os documentos
        llm: O modelo LLM (ChatOpenAI)
        question: A pergunta do usuário (string)
    
    Returns:
        dict: {
            'answer': str - Resposta gerada,
            'sources': list - Lista de fontes consultadas [{file, page, preview}]
        }
    """
    try:
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        # Busca documentos relevantes
        docs = retriever.invoke(question)
        
        # Monta o contexto
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Cria o prompt otimizado para linguagem simples
        prompt = f"""Você é um assistente especializado em explicar documentos legais e fiscais de forma SIMPLES e CLARA para pessoas que não têm conhecimento técnico.

INSTRUÇÕES IMPORTANTES:
1. Use linguagem simples e cotidiana, evite jargões técnicos
2. Explique como se estivesse conversando com um amigo
3. Use exemplos práticos quando possível
4. Divida informações complexas em tópicos curtos
5. Se mencionar termos técnicos, explique-os de forma simples
6. Seja direto e objetivo
7. Use analogias se ajudar na compreensão
8. Se não souber a resposta com base nos documentos, diga claramente

Documentos para consulta:
{context}

Pergunta: {question}

Resposta clara e simples:"""
        
        # Faz a pergunta ao modelo
        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages)
        
        # Prepara as fontes de forma simplificada
        sources = []
        for doc in docs:
            sources.append({
                'file': Path(doc.metadata.get('source', 'Desconhecido')).name,
                'page': doc.metadata.get('page', 'N/A'),
                'preview': doc.page_content[:200].replace('\n', ' ')
            })
        
        return {
            'answer': response.content,
            'sources': sources
        }
        
    except Exception as e:
        print(f"❌ Erro ao processar pergunta: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_rag_interactive(vector_store, llm):
    """Testa o RAG com input do usuário"""
    try:
        print("\n" + "="*60)
        print("💬 ASSISTENTE DE DOCUMENTOS")
        print("="*60)
        print("Faça perguntas sobre MEI, direitos do consumidor e mais!")
        print("Digite 'sair' para encerrar\n")
        
        while True:
            question = input("❓ Sua pergunta: ").strip()
            
            if question.lower() in ['sair', 'exit', 'quit', 'q']:
                print("\n👋 Até logo!")
                break
            
            if not question:
                print("⚠️ Por favor, digite uma pergunta.\n")
                continue
            
            print("\n🔍 Buscando informações...\n")
            
            result = query_documents(vector_store, llm, question)
            
            if result:
                print("💡 RESPOSTA:")
                print("-" * 60)
                print(result['answer'])
                print("-" * 60)
                
                # Mostra fontes de forma simplificada
                if result['sources']:
                    print(f"\n📚 Informações baseadas em {len(result['sources'])} documento(s):")
                    for i, source in enumerate(result['sources'], 1):
                        print(f"   • {source['file']} (pág. {source['page']})")
                
                print("\n" + "="*60 + "\n")
            else:
                print("❌ Não consegui processar sua pergunta. Tente novamente.\n")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n👋 Até logo!")
        return True
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal que coordena o processo RAG"""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ Chave da OpenAI não encontrada!")
            print("💡 Configure o arquivo .env com sua chave API")
            return False
        
        print("✅ Conectado!")
        print("🚀 Inicializando assistente...")
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        
        vector_store = load_vector_store()
        if vector_store:
            print("✅ Documentos carregados da memória")
        else:
            print("\n📚 Primeira execução - processando documentos...")
            documents = load_documents_from_data()
            if not documents:
                print("\n⚠️ Nenhum documento encontrado na pasta 'data'")
                return False
            chunks = split_documents(documents)
            if not chunks:
                print("\n⚠️ Erro ao processar documentos")
                return False
            print(f"\n📊 Processados: {len(documents)} páginas em {len(chunks)} partes")
            vector_store = create_vector_store(chunks)
            if not vector_store:
                print("\n⚠️ Erro ao criar índice de busca")
                return False
            save_vector_store(vector_store)
        
        # Inicia modo interativo
        test_rag_interactive(vector_store, llm)
        
        return True
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("� ASSISTENTE INTELIGENTE DE DOCUMENTOS")
    print("=" * 60)
    main()
    print("\n" + "=" * 60)

