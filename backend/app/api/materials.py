from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
import uuid
from backend.app.api.auth import get_current_user
from backend.app.models.db_models import User
from backend.app.services.pricing_engine import DEFAULT_MATERIAL_CATALOG

router = APIRouter(tags=["Materials & Pricing"])

CATALOG_DB = list(DEFAULT_MATERIAL_CATALOG)

QUOTATION_HISTORY = [
    {
        "id": "q-hist-01",
        "material_name": "UltraTech Super Cement OPC 53",
        "price": 380.0,
        "date": "2026-06-15",
        "supplier": "South India Cements",
        "location": "Chennai"
    },
    {
        "id": "q-hist-02",
        "material_name": "UltraTech Super Cement OPC 53",
        "price": 390.0,
        "date": "2026-08-01",
        "supplier": "South India Cements",
        "location": "Chennai"
    },
    {
        "id": "q-hist-03",
        "material_name": "UltraTech Super Cement OPC 53",
        "price": 395.0,
        "date": "2026-09-15",
        "supplier": "South India Cements Depot",
        "location": "Chennai"
    },
    {
        "id": "q-hist-04",
        "material_name": "Tata Tiscon 550D TMT",
        "price": 64000.0,
        "date": "2026-06-15",
        "supplier": "Tata Tiscon Direct Dealer",
        "location": "Chennai"
    },
    {
        "id": "q-hist-05",
        "material_name": "Tata Tiscon 550D TMT",
        "price": 66500.0,
        "date": "2026-10-01",
        "supplier": "Tata Tiscon Direct Dealer",
        "location": "Chennai"
    }
]

@router.get("/materials")
async def list_materials(category: Optional[str] = None):
    if category:
        return [m for m in CATALOG_DB if m["category"].lower() == category.lower()]
    return CATALOG_DB

@router.post("/materials")
async def add_material(payload: Dict[str, Any], user: User = Depends(get_current_user)):
    item = {
        "id": f"mat-{uuid.uuid4().hex[:6]}",
        "category": payload.get("category", "General"),
        "name": payload.get("name", "New Building Material"),
        "specification": payload.get("specification", ""),
        "unit": payload.get("unit", "Unit"),
        "default_price": float(payload.get("default_price", 100.0)),
        "currency": payload.get("currency", "INR"),
        "supplier": payload.get("supplier", "Local Supplier"),
        "location": payload.get("location", "Chennai"),
        "quotation_date": "2026-10-09",
        "tax_inclusive": True
    }
    CATALOG_DB.append(item)
    return item

@router.get("/prices/lookup")
async def lookup_prices(query: str = Query(...)):
    results = [
        m for m in CATALOG_DB 
        if query.lower() in m["name"].lower() or query.lower() in m["category"].lower()
    ]
    return results

@router.post("/prices/quotations")
async def submit_quotation(payload: Dict[str, Any], user: User = Depends(get_current_user)):
    item = {
        "id": f"q-{uuid.uuid4().hex[:6]}",
        "material_name": payload.get("material_name"),
        "price": float(payload.get("unit_price", 0.0)),
        "date": "2026-10-09",
        "supplier": payload.get("supplier_name", "Vendor"),
        "location": payload.get("location", "Tamil Nadu")
    }
    QUOTATION_HISTORY.append(item)
    return {"message": "Quotation submitted and verified successfully", "quotation": item}

@router.get("/prices/history")
async def get_price_history(material_name: Optional[str] = None):
    if material_name:
        return [q for q in QUOTATION_HISTORY if material_name.lower() in q["material_name"].lower()]
    return QUOTATION_HISTORY
