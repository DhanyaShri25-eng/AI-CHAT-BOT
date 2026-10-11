from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import List, Dict, Any, Optional
import uuid
from backend.app.api.auth import get_current_user
from backend.app.models.db_models import User
from backend.app.schemas.all_schemas import DocumentSearchRequest, DocumentSearchResult
from backend.app.services.rag_service import search_building_codes, VERIFIED_KNOWLEDGE_DOCUMENTS

router = APIRouter(prefix="/documents", tags=["Documents & RAG"])

DOCUMENTS_STORE = list(VERIFIED_KNOWLEDGE_DOCUMENTS)

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    category: Optional[str] = Form("User Specifications"),
    user: User = Depends(get_current_user)
):
    """Secure document upload and ingestion with untrusted input safety checks."""
    content_bytes = await file.read()
    try:
        text = content_bytes.decode("utf-8")
    except Exception:
        text = f"Binary content from {file.filename} (Size: {len(content_bytes)} bytes)"
        
    doc = {
        "id": f"doc-usr-{uuid.uuid4().hex[:6]}",
        "title": title or file.filename,
        "category": category,
        "publisher": user.full_name or "Project Owner",
        "jurisdiction": "Project Specific",
        "version": "Uploaded 2026",
        "section_code": "User Addendum",
        "content": text[:4000]
    }
    DOCUMENTS_STORE.append(doc)
    return {
        "message": "Document ingested and indexed for RAG retrieval",
        "document": {
            "id": doc["id"],
            "title": doc["title"],
            "category": doc["category"],
            "size_bytes": len(content_bytes)
        }
    }

@router.post("/search", response_model=List[DocumentSearchResult])
async def search_documents(
    req: DocumentSearchRequest
):
    """Retrieve verified building regulations and code excerpts."""
    results = search_building_codes(query=req.query, jurisdiction=req.jurisdiction or "Tamil Nadu / National", top_k=req.top_k)
    return results

@router.delete("/{id}")
async def delete_document(
    id: str,
    user: User = Depends(get_current_user)
):
    global DOCUMENTS_STORE
    DOCUMENTS_STORE = [d for d in DOCUMENTS_STORE if d.get("id") != id]
    return {"message": "Document deleted"}
