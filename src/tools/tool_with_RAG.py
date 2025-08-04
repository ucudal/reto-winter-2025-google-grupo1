from typing import List, Dict, Any, Optional
import numpy as np
import os
import google.generativeai as genai
from google.cloud import bigquery
from google.oauth2 import service_account
from pydantic import BaseModel, Field
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv(Path(__file__).parent.parent.parent / '.env')

# Funciones para cargar variables de entorno
def get_google_api_key():
    return os.getenv('GOOGLE_CLOUD_API_KEY')

def get_project_id():
    return os.getenv('PROJECT_ID')

def get_dataset():
    return os.getenv('DATASET')

def get_table():
    return os.getenv('TABLE')


class Document(BaseModel):
    """Modelo para representar un documento con su contenido y embedding"""
    id: str
    content: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RAGQuery(BaseModel):
    """Modelo para representar una consulta RAG"""
    query: str
    top_k: int = Field(default=3, description="Número de documentos más relevantes a recuperar")
    similarity_threshold: float = Field(default=0.7, description="Umbral de similitud mínimo")


class RAGResponse(BaseModel):
    """Modelo para representar la respuesta RAG"""
    answer: str
    relevant_documents: List[Document]
    similarity_scores: List[float]
    context_used: str


class RAGTool:
    """Herramienta RAG que utiliza embeddings de Google y Gemini para generar respuestas"""
    
    def __init__(self):
        genai.configure(api_key=get_google_api_key())
        self.embedding_model = "models/embedding-001"
        self.generation_model = "gemini-2.0-flash-exp"
        self.documents: List[Document] = []
    
    def _get_embedding(self, text: str) -> List[float]:
        """Obtiene el embedding de un texto usando Google's embedding model"""
        response = genai.embed_content(
            model=self.embedding_model,
            content=text,
            task_type="retrieval_query"
        )
        return response['embedding']
    
    def _cosine_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calcula la similitud coseno entre dos embeddings"""
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def load_documents_from_bigquery(self, limit: Optional[int] = None) -> None:
        """Carga documentos desde BigQuery usando service account"""
        try:
            # Cargar credenciales del service account
            credentials_path = Path(__file__).parent.parent.parent / "adept-storm-467519-j4-ce5c1b07d879.json"
            credentials = service_account.Credentials.from_service_account_file(str(credentials_path))
            
            # Inicializar cliente de BigQuery
            project_id = get_project_id()
            bq_client = bigquery.Client(credentials=credentials, project=project_id)
            
            # Construir consulta
            dataset = get_dataset()
            table = get_table()
            
            print(f"🔍 Consultando tabla: {project_id}.{dataset}.{table}")
            
            query = f"""
            SELECT 
                document_id,
                fragment_text,
                embedding,
                created_at
            FROM `{project_id}.{dataset}.{table}`
            ORDER BY created_at DESC
            """
            
            if limit:
                query += f" LIMIT {limit}"
            
            print("📊 Ejecutando consulta...")
            
            # Ejecutar consulta
            query_job = bq_client.query(query)
            results = query_job.result()
            
            # Procesar resultados
            count = 0
            for row in results:
                document = Document(
                    id=f"{row.document_id}_{count}",
                    content=row.fragment_text,
                    embedding=row.embedding,
                    metadata={
                        "document_id": row.document_id,
                        "created_at": row.created_at.isoformat() if row.created_at else None
                    }
                )
                self.documents.append(document)
                count += 1
                
            print(f"✅ Cargados {count} documentos desde BigQuery")
            
            if count == 0:
                print("⚠️ No se encontraron documentos en la tabla")
            
        except Exception as e:
            print(f"❌ Error cargando documentos desde BigQuery: {e}")
            raise e
    
    def _retrieve_relevant_documents(self, query: str, top_k: int, similarity_threshold: float) -> tuple[List[Document], List[float]]:
        """Recupera los documentos más relevantes basándose en similitud de embeddings"""
        if not self.documents:
            return [], []
        
        query_embedding = self._get_embedding(query)
        
        # Calcular similitudes
        similarities = []
        for doc in self.documents:
            if doc.embedding:
                similarity = self._cosine_similarity(query_embedding, doc.embedding)
                similarities.append((doc, similarity))
        
        # Filtrar por umbral y ordenar por similitud
        filtered_similarities = [
            (doc, sim) for doc, sim in similarities 
            if sim >= similarity_threshold
        ]
        
        # Ordenar por similitud descendente y tomar top_k
        filtered_similarities.sort(key=lambda x: x[1], reverse=True)
        top_documents = filtered_similarities[:top_k]
        
        if not top_documents:
            return [], []
        
        documents, scores = zip(*top_documents)
        return list(documents), list(scores)
    
    def _create_context_prompt(self, query: str, relevant_docs: List[Document]) -> str:
        """Crea un prompt con contexto para la generación de respuestas"""
        if not relevant_docs:
            return f"Consulta: {query}\n\nNo se encontraron documentos relevantes para responder esta consulta."
        
        context_parts = []
        for i, doc in enumerate(relevant_docs, 1):
            context_parts.append(f"Documento {i}:\n{doc.content}\n")
        
        context = "\n".join(context_parts)
        
        prompt = f"""Basándote en los siguientes documentos, responde la consulta del usuario de manera precisa y completa. 
Si la información no está en los documentos, indícalo claramente.

Documentos de referencia:
{context}

Consulta del usuario: {query}

Instrucciones:
1. Responde únicamente basándote en la información proporcionada en los documentos
2. Cita específicamente qué documentos usaste para cada parte de tu respuesta
3. Si la consulta no puede ser respondida con los documentos disponibles, indícalo claramente
4. Proporciona una respuesta estructurada y bien organizada

Respuesta:"""
        
        return prompt
    
    def query(self, rag_query: RAGQuery) -> RAGResponse:
        """Ejecuta una consulta RAG completa"""
        # Recuperar documentos relevantes
        relevant_docs, similarity_scores = self._retrieve_relevant_documents(
            rag_query.query, 
            rag_query.top_k, 
            rag_query.similarity_threshold
        )
        
        # Crear prompt con contexto
        context_prompt = self._create_context_prompt(rag_query.query, relevant_docs)
        
        # Generar respuesta usando Gemini
        model = genai.GenerativeModel(self.generation_model)
        response = model.generate_content(
            contents=context_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                top_p=0.8,
                top_k=40,
                max_output_tokens=1024,
            )
        )
        
        answer = response.text if response.text else "No se pudo generar una respuesta."
        
        return RAGResponse(
            answer=answer,
            relevant_documents=relevant_docs,
            similarity_scores=similarity_scores,
            context_used=context_prompt
        )


# Función principal para consultas RAG con BigQuery
def query_rag_with_bigquery(
    user_query: str, 
    top_k: int = 5, 
    similarity_threshold: float = 0.3,
    max_documents: int = 1000
) -> RAGResponse:
    """
    Función principal para realizar consultas RAG conectadas con BigQuery.
    
    Args:
        user_query: La consulta del usuario
        top_k: Número de documentos más relevantes a recuperar
        similarity_threshold: Umbral de similitud mínimo (0.0 a 1.0)
        max_documents: Máximo número de documentos a cargar desde BigQuery
        
    Returns:
        RAGResponse: Respuesta completa del sistema RAG
    """
    try:
        print(f"🔍 Procesando consulta: '{user_query}'")
        
        # Crear instancia de RAGTool
        rag_tool = RAGTool()
        
        # Cargar documentos desde BigQuery
        print("📥 Cargando documentos desde BigQuery...")
        rag_tool.load_documents_from_bigquery(limit=max_documents)
        
        # Crear consulta RAG
        rag_query = RAGQuery(
            query=user_query,
            top_k=top_k,
            similarity_threshold=similarity_threshold
        )
        
        # Ejecutar consulta
        print("🤖 Generando respuesta...")
        response = rag_tool.query(rag_query)
        
        print(f"✅ Respuesta generada con {len(response.relevant_documents)} documentos relevantes")
        
        return response
        
    except Exception as e:
        print(f"❌ Error en consulta RAG: {e}")
        # Retornar respuesta de error
        return RAGResponse(
            answer=f"Lo siento, ocurrió un error al procesar tu consulta: {str(e)}",
            relevant_documents=[],
            similarity_scores=[],
            context_used=""
        )


# Función simplificada para uso directo
def ask_question(question: str) -> str:
    """
    Función simplificada para hacer una pregunta al sistema RAG.
    
    Args:
        question: La pregunta del usuario
        
    Returns:
        str: La respuesta generada
    """
    response = query_rag_with_bigquery(question)
    return response.answer