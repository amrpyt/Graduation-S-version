from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from agno.dependencies import get_current_user
from agno.models import User
from typing import List, Optional, Dict
from pydantic import BaseModel
from services.rag_service import RAGService
from config import Settings

settings = Settings()
router = APIRouter()
rag_service = RAGService()

class Document(BaseModel):
    content: str
    metadata: Optional[Dict] = None

class Query(BaseModel):
    question: str
    k: Optional[int] = 3

class DeleteFilter(BaseModel):
    metadata: Optional[Dict] = None

@router.post("/documents/add")
async def add_documents(
    documents: List[Document],
    current_user: User = Depends(get_current_user)
):
    """Add documents to the RAG system"""
    try:
        docs = [{
            "content": doc.content,
            "metadata": {
                **(doc.metadata or {}),
                "user_id": current_user.id
            }
        } for doc in documents]
        
        success = await rag_service.add_documents(docs)
        if success:
            return {"message": "Documents added successfully"}
        raise HTTPException(status_code=500, detail="Failed to add documents")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query")
async def query(
    query: Query,
    current_user: User = Depends(get_current_user)
):
    """Query the RAG system"""
    try:
        response = await rag_service.query(
            question=query.question,
            k=query.k,
            user_id=current_user.id
        )
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/delete")
async def delete_documents(
    filter: DeleteFilter,
    current_user: User = Depends(get_current_user)
):
    """Delete documents from the RAG system"""
    try:
        metadata = {
            **(filter.metadata or {}),
            "user_id": current_user.id
        }
        success = await rag_service.delete_documents(metadata)
        if success:
            return {"message": "Documents deleted successfully"}
        raise HTTPException(status_code=500, detail="Failed to delete documents")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload a text file to the RAG system"""
    try:
        content = await file.read()
        text_content = content.decode("utf-8")
        doc = {
            "content": text_content,
            "metadata": {
                "filename": file.filename,
                "content_type": file.content_type,
                "user_id": current_user.id
            }
        }
        success = await rag_service.add_documents([doc])
        if success:
            return {"message": "File uploaded and processed successfully"}
        raise HTTPException(status_code=500, detail="Failed to process file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 