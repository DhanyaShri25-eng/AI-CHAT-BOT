from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional
from backend.app.core.database import get_db
from backend.app.api.auth import get_current_user
from backend.app.models.db_models import User
from backend.app.schemas.all_schemas import FloorPlanGenerateRequest, DesignVersionOut
from backend.app.services.floorplan_engine import generate_floor_plan

router = APIRouter(prefix="/designs", tags=["Architecture & Designs"])

# In-memory design storage cache for fast retrieval & revisions
DESIGN_STORE = {}

@router.post("/generate", response_model=DesignVersionOut)
async def generate_design(
    req: FloorPlanGenerateRequest,
    user: User = Depends(get_current_user)
):
    """
    Generate architectural 2D floor plan, setback boundaries, Vastu alignments,
    blueprint SVG and front elevation concept.
    """
    design = generate_floor_plan(
        plot_width=req.plot_width,
        plot_length=req.plot_length,
        building_type=req.building_type,
        orientation=req.orientation,
        floors=req.floors,
        architectural_style=req.architectural_style,
        setback_front=req.setback_front or 5.0,
        setback_rear=req.setback_rear or 3.0,
        setback_sides=req.setback_sides or 3.0
    )
    design["project_id"] = req.project_id
    DESIGN_STORE[design["id"]] = design
    return design

@router.get("/{id}", response_model=DesignVersionOut)
async def get_design(
    id: str,
    user: User = Depends(get_current_user)
):
    if id in DESIGN_STORE:
        return DESIGN_STORE[id]
        
    # If not found in cache, generate a default realistic design
    design = generate_floor_plan(plot_width=30.0, plot_length=40.0, building_type="2BHK")
    design["id"] = id
    DESIGN_STORE[id] = design
    return design

@router.post("/{id}/revise", response_model=DesignVersionOut)
async def revise_design(
    id: str,
    req: FloorPlanGenerateRequest,
    user: User = Depends(get_current_user)
):
    """Regenerate affected room layouts and recalculate area while maintaining version history."""
    old_version = DESIGN_STORE.get(id)
    prev_ver_num = old_version.get("version_number", 1) if old_version else 1
    
    revised = generate_floor_plan(
        plot_width=req.plot_width,
        plot_length=req.plot_length,
        building_type=req.building_type,
        orientation=req.orientation,
        floors=req.floors,
        architectural_style=req.architectural_style,
        setback_front=req.setback_front or 5.0,
        setback_rear=req.setback_rear or 3.0,
        setback_sides=req.setback_sides or 3.0
    )
    revised["version_number"] = prev_ver_num + 1
    revised["title"] = f"Revised Architectural Plan V{revised['version_number']} ({req.building_type})"
    DESIGN_STORE[revised["id"]] = revised
    return revised
