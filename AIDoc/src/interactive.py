"""
Módulo para interface interativa com o usuário
"""
from .rag_query import query_documents


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
