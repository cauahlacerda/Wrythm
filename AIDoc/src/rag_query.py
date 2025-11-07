"""
Módulo para processamento de perguntas usando RAG
"""
from pathlib import Path
from langchain_core.messages import HumanMessage


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
