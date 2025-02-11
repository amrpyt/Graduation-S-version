from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import List, Dict, Optional
from pydantic import BaseModel
from config import Settings
from rag_agent import RAGAgent

# Initialize settings and agent
settings = Settings()
rag_agent = RAGAgent()

# Create FastAPI app
app = FastAPI(
    title="RAG API",
    description="RAG Application with Supabase and Gemini",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

# Define request models
class Document(BaseModel):
    content: str
    metadata: Optional[Dict] = None

class Query(BaseModel):
    question: str
    k: Optional[int] = 3

@app.post("/documents/add")
async def add_documents(documents: List[Document]):
    """Add documents to the RAG system"""
    docs = [{"content": doc.content, "metadata": doc.metadata} for doc in documents]
    success = await rag_agent.add_documents(docs)
    return {"success": success}

@app.post("/query")
async def query(query: Query):
    """Query the RAG system"""
    response = await rag_agent.query(question=query.question, k=query.k)
    return {"answer": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 