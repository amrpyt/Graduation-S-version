from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.memory import Memory
from agno.tools import VectorStore
from agno.models import GeminiModel
from typing import List, Dict, Optional
from config import Settings
from supabase import create_client, Client

settings = Settings()

class RAGAgent(Agent):
    def __init__(self):
        # Initialize the base agent with Gemini model
        super().__init__(
            model=GeminiModel(
                api_key=settings.google_api_key,
                model_name=settings.gemini_model,
                temperature=settings.gemini_temperature
            )
        )
        
        # Initialize Supabase client
        self.supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
        
        # Initialize vector store using Supabase pgvector
        self.vector_store = VectorStore(
            provider="supabase",
            client=self.supabase,
            table_name=settings.db_collection,
            embedding_model=settings.gemini_embedding_model
        )
        
        # Initialize knowledge base
        self.knowledge = Knowledge(
            vector_store=self.vector_store,
            chunk_size=8000,
            chunk_overlap=800
        )
        
        # Initialize memory for user sessions
        self.memory = Memory(
            storage_type="supabase",
            url=settings.supabase_url,
            key=settings.supabase_key
        )

    async def add_documents(self, documents: List[Dict]) -> bool:
        """Add documents to the knowledge base"""
        try:
            # Add documents to knowledge store with embeddings
            self.knowledge.add_documents(documents)
            return True
        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            return False

    async def query(
        self,
        question: str,
        k: int = 3,
        user_id: Optional[str] = None
    ) -> str:
        """Query the RAG system using similarity search"""
        try:
            # Get relevant context using pgvector similarity search
            context = self.knowledge.search(
                query=question,
                k=k,
                filter={"user_id": user_id} if user_id else None
            )
            
            # Get chat history from memory
            chat_history = self.memory.get_chat_history(user_id) if user_id else []
            
            # Generate response using the model
            response = await self.generate(
                prompt=f"Based on the following context:\n{context}\n\nQuestion: {question}",
                chat_history=chat_history
            )
            
            # Store interaction in memory
            if user_id:
                self.memory.store_interaction(
                    user_id=user_id,
                    question=question,
                    answer=response
                )
            
            return response
        except Exception as e:
            print(f"Error querying: {str(e)}")
            raise

    async def delete_documents(self, metadata: Dict) -> bool:
        """Delete documents from the knowledge base"""
        try:
            self.knowledge.delete_documents(metadata)
            return True
        except Exception as e:
            print(f"Error deleting documents: {str(e)}")
            return False
