from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any
from backend.app.core.database import get_db
from backend.app.api.auth import get_current_user
from backend.app.models.db_models import User, Project, ProjectRequirement
from backend.app.schemas.all_schemas import ProjectCreate, ProjectUpdate, ProjectOut

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("", response_model=List[ProjectOut])
async def list_projects(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Project).where(Project.user_id == user.id).order_by(Project.created_at.desc())
    res = await db.execute(stmt)
    projects = res.scalars().all()
    
    # If user has no projects, create a default realistic sample project
    if not projects:
        default_proj = Project(
            user_id=user.id,
            name="Greenwood Villa Residence",
            description="3BHK G+1 Contemporary Villa with Vastu layout and modular kitchen",
            building_type="3BHK Duplex",
            location="OMR, Chennai, Tamil Nadu",
            plot_length=40.0,
            plot_width=30.0,
            plot_area=1200.0,
            built_up_area=1800.0,
            floors=2,
            rooms=6,
            target_budget=4500000.0,
            current_stage="Architecture"
        )
        db.add(default_proj)
        await db.commit()
        await db.refresh(default_proj)
        return [default_proj]
        
    return projects

@router.post("", response_model=ProjectOut)
async def create_project(
    req: ProjectCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    plot_area = req.plot_area or (req.plot_length * req.plot_width)
    built_up = req.built_up_area or (plot_area * 0.75 * req.floors)
    
    project = Project(
        user_id=user.id,
        name=req.name,
        description=req.description,
        building_type=req.building_type,
        location=req.location,
        plot_length=req.plot_length,
        plot_width=req.plot_width,
        plot_area=plot_area,
        plot_area_unit=req.plot_area_unit,
        built_up_area=built_up,
        floors=req.floors,
        target_budget=req.target_budget or 4500000.0
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

@router.get("/{id}", response_model=ProjectOut)
async def get_project(
    id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Project).where(Project.id == id, Project.user_id == user.id)
    res = await db.execute(stmt)
    proj = res.scalar_one_or_none()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj

@router.patch("/{id}", response_model=ProjectOut)
async def update_project(
    id: str,
    req: ProjectUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Project).where(Project.id == id, Project.user_id == user.id)
    res = await db.execute(stmt)
    proj = res.scalar_one_or_none()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
        
    for k, v in req.dict(exclude_unset=True).items():
        setattr(proj, k, v)
        
    await db.commit()
    await db.refresh(proj)
    return proj

@router.delete("/{id}")
async def delete_project(
    id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Project).where(Project.id == id, Project.user_id == user.id)
    res = await db.execute(stmt)
    proj = res.scalar_one_or_none()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.delete(proj)
    await db.commit()
    return {"message": "Project deleted successfully"}
