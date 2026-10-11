from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from backend.app.services.picture_service import (
    search_and_recommend_pictures,
    get_picture_by_id,
    PICTURE_CATALOG
)

router = APIRouter(prefix="/pictures", tags=["Architectural Picture Recommendations"])

class RecommendPicturesRequest(BaseModel):
    query: str
    category: Optional[str] = None
    style: Optional[str] = None
    limit: Optional[int] = 4

@router.get("/")
async def list_pictures(
    query: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    style: Optional[str] = Query(None),
    limit: int = Query(12)
):
    """List or search pictures and architectural visual designs."""
    if query or category or style:
        results = search_and_recommend_pictures(
            query=query or "",
            category=category,
            style=style,
            limit=limit
        )
        return results
    return PICTURE_CATALOG[:limit]

@router.post("/recommend")
async def recommend_pictures_endpoint(req: RecommendPicturesRequest):
    """Recommend architectural pictures based on conversation query or user prompt."""
    results = search_and_recommend_pictures(
        query=req.query,
        category=req.category,
        style=req.style,
        limit=req.limit or 4
    )
    return {"pictures": results, "count": len(results)}

@router.get("/categories")
async def list_categories():
    """Return available categories and styles in the visual recommendation catalog."""
    categories = sorted(list(set(p["category"] for p in PICTURE_CATALOG)))
    styles = sorted(list(set(p["style"] for p in PICTURE_CATALOG)))
    return {"categories": categories, "styles": styles}

@router.get("/{picture_id}")
async def get_picture_details(picture_id: str):
    """Retrieve full specifications and high-res details for a picture."""
    pic = get_picture_by_id(picture_id)
    if not pic:
        raise HTTPException(status_code=404, detail="Picture not found")
    return pic
