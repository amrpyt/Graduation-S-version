from langchain.embeddings import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from supabase import create_client, Client
from typing import List, Dict, Optional
from config import Settings

settings = Settings()

class RAGService:
    def __init__(self):
        # Initialize Supabase client
        self.supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
        
        # Initialize embeddings with Gemini
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.gemini_embedding_model,
            google_api_key=settings.google_api_key
        )
        
        # Initialize vector store
        self.vector_store = SupabaseVectorStore(
            client=self.supabase,
            embedding=self.embeddings,
            table_name=settings.db_collection,
            query_name=settings.embeddings_collection
        )
        
        # Initialize text splitter with larger chunk size for Gemini's context window
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=8000,  # Increased for Gemini's larger context
            chunk_overlap=800
        )
        
        # Initialize Gemini 2.0 Flash
        self.llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=settings.gemini_temperature,
            top_p=settings.gemini_top_p,
            top_k=settings.gemini_top_k,
            max_output_tokens=settings.gemini_max_output_tokens,
        )
        
        # Initialize retrieval chain with streaming support
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 5}  # Increased for better context
            ),
            return_source_documents=True,
            verbose=True
        )

    async def add_documents(self, documents: List[Dict]) -> bool:
        try:
            # Split documents into chunks
            texts = []
            metadatas = []
            
            for doc in documents:
                chunks = self.text_splitter.split_text(doc["content"])
                texts.extend(chunks)
                metadatas.extend([doc["metadata"]] * len(chunks))
            
            # Add to vector store
            self.vector_store.add_texts(
                texts=texts,
                metadatas=metadatas
            )
            
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
        try:
            # Prepare search filter if user_id is provided
            search_kwargs = {}
            if user_id:
                search_kwargs["filter"] = {"user_id": user_id}
            
            # Get response from QA chain
            response = self.qa_chain({
                "question": question,
                "chat_history": [],
                "search_kwargs": search_kwargs
            })
            
            return response["answer"]
        except Exception as e:
            print(f"Error querying: {str(e)}")
            raise

    async def delete_documents(self, metadata: Dict) -> bool:
        try:
            # Delete documents from Supabase
            self.supabase.table(settings.db_collection)\
                .delete()\
                .match(metadata)\
                .execute()
            
            return True
        except Exception as e:
            print(f"Error deleting documents: {str(e)}")
            return False 