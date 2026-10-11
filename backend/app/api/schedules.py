from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
import uuid
from backend.app.api.auth import get_current_user
from backend.app.models.db_models import User
from backend.app.schemas.all_schemas import ScheduleGenerateRequest
from backend.app.services.schedule_engine import generate_construction_schedule

router = APIRouter(prefix="/schedules", tags=["Scheduling"])

SCHEDULE_STORE = {}

@router.post("/generate")
async def generate_schedule(
    req: ScheduleGenerateRequest,
    user: User = Depends(get_current_user)
):
    sch = generate_construction_schedule(
        built_up_area=req.built_up_area,
        floors=req.floors,
        start_date_str=req.start_date,
        contractor_speed=req.contractor_speed,
        monsoon_factor=req.monsoon_factor
    )
    sch_id = str(uuid.uuid4())
    sch["id"] = sch_id
    sch["project_id"] = req.project_id
    SCHEDULE_STORE[sch_id] = sch
    return sch

@router.get("/{id}")
async def get_schedule(
    id: str,
    user: User = Depends(get_current_user)
):
    if id in SCHEDULE_STORE:
        return SCHEDULE_STORE[id]
        
    sch = generate_construction_schedule(built_up_area=1800.0, floors=2)
    sch["id"] = id
    SCHEDULE_STORE[id] = sch
    return sch

@router.patch("/{id}/tasks/{task_id}")
async def update_schedule_task(
    id: str,
    task_id: str,
    payload: Dict[str, Any],
    user: User = Depends(get_current_user)
):
    sch = SCHEDULE_STORE.get(id)
    if not sch:
        sch = generate_construction_schedule(built_up_area=1800.0, floors=2)
        sch["id"] = id
        SCHEDULE_STORE[id] = sch
        
    for task in sch["tasks"]:
        if task["id"] == task_id:
            if "status" in payload:
                task["status"] = payload["status"]
            if "delay_risk_level" in payload:
                task["delay_risk_level"] = payload["delay_risk_level"]
            return {"message": "Task updated successfully", "task": task}
            
    raise HTTPException(status_code=404, detail="Task not found")
