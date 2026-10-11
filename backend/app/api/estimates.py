from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
import uuid
from backend.app.api.auth import get_current_user
from backend.app.models.db_models import User
from backend.app.schemas.all_schemas import MaterialCalculateRequest, CostEstimateOut
from backend.app.services.pricing_engine import calculate_full_cost_estimate

router = APIRouter(prefix="/estimates", tags=["Estimation"])

ESTIMATE_STORE = {}

@router.post("/calculate", response_model=CostEstimateOut)
async def calculate_estimate(
    req: MaterialCalculateRequest,
    user: User = Depends(get_current_user)
):
    """Calculate deterministic itemized construction estimate with low, expected, and high budgets."""
    est = calculate_full_cost_estimate(
        built_up_area=req.built_up_area,
        floors=req.floors,
        structure_type=req.structure_type,
        wall_type=req.wall_type,
        construction_quality=req.construction_quality
    )
    est["id"] = str(uuid.uuid4())
    est["project_id"] = req.project_id
    ESTIMATE_STORE[est["id"]] = est
    return est

@router.get("/{id}", response_model=CostEstimateOut)
async def get_estimate(
    id: str,
    user: User = Depends(get_current_user)
):
    if id in ESTIMATE_STORE:
        return ESTIMATE_STORE[id]
        
    est = calculate_full_cost_estimate(built_up_area=1800.0, floors=2)
    est["id"] = id
    ESTIMATE_STORE[id] = est
    return est

@router.post("/compare")
async def compare_estimates(
    req: Dict[str, Any],
    user: User = Depends(get_current_user)
):
    """Compare Economy vs Standard Premium vs Luxury specifications for a given built-up area."""
    built_up = float(req.get("built_up_area", 1800.0))
    floors = int(req.get("floors", 2))
    
    economy = calculate_full_cost_estimate(built_up_area=built_up, floors=floors, construction_quality="Economy")
    standard = calculate_full_cost_estimate(built_up_area=built_up, floors=floors, construction_quality="Standard")
    premium = calculate_full_cost_estimate(built_up_area=built_up, floors=floors, construction_quality="Standard Premium")
    luxury = calculate_full_cost_estimate(built_up_area=built_up, floors=floors, construction_quality="Luxury")
    
    return {
        "built_up_area": built_up,
        "floors": floors,
        "comparisons": [
            {"tier": "Economy", "total": economy["total_expected"], "rate_sqft": economy["rate_per_sqft"], "highlights": "Red bricks, standard tiles, emulsion paint"},
            {"tier": "Standard", "total": standard["total_expected"], "rate_sqft": standard["rate_per_sqft"], "highlights": "AAC blocks, vitrified 600x600, premium emulsion"},
            {"tier": "Standard Premium", "total": premium["total_expected"], "rate_sqft": premium["rate_per_sqft"], "highlights": "Fe550D TMT, 800x800 vitrified, Asian Royale, UPVC windows"},
            {"tier": "Luxury", "total": luxury["total_expected"], "rate_sqft": luxury["rate_per_sqft"], "highlights": "Italian marble/granite, Teak wood, automated fixtures, solar heating"}
        ]
    }
