import asyncio
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel

from backend.app.services.training_service import (
    get_training_dataset_stats,
    export_training_dataset,
    start_fine_tuning_job,
    get_job_status,
    list_registered_models,
    set_active_model,
    log_conversation_turn
)
from backend.app.services.dataset_trainer import (
    get_kaggle_training_status,
    run_pytorch_kaggle_training,
    KAGGLE_DATASETS_INFO
)

router = APIRouter(prefix="/training", tags=["Model Training & Alignment"])

class FeedbackRequest(BaseModel):
    prompt: str
    response: str
    rating: int # 1 for thumbs up, -1 for thumbs down
    correction: Optional[str] = None
    user_id: Optional[str] = "default"

class KaggleTrainRequest(BaseModel):
    epochs: Optional[int] = 5
    batch_size: Optional[int] = 16
    learning_rate: Optional[float] = 0.0003

class FineTuneRequest(BaseModel):
    base_model: Optional[str] = "buildwise-llama3-construction-8b"
    epochs: Optional[int] = 3
    learning_rate: Optional[float] = 0.0002
    lora_rank: Optional[int] = 64

class SelectModelRequest(BaseModel):
    model_id: str

@router.get("/kaggle/status")
async def get_kaggle_status():
    """Retrieve datasets information, PyTorch training progress, loss history."""
    return get_kaggle_training_status()

@router.post("/kaggle/train")
async def train_on_kaggle_datasets(req: KaggleTrainRequest):
    """
    Train the model using:
    1. Adil Mohammed: Floor Plan Images and Their Details
    2. Bouygues Construction Challenge: BIM structural takeoffs & scheduling
    """
    asyncio.create_task(run_pytorch_kaggle_training(
        epochs=req.epochs or 5,
        batch_size=req.batch_size or 16,
        learning_rate=req.learning_rate or 0.0003
    ))
    return {
        "message": "PyTorch training started on Kaggle datasets (Floor Plan Images & Bouygues Construction).",
        "datasets": list(KAGGLE_DATASETS_INFO.keys()),
        "status": "training"
    }

@router.get("/stats")
async def get_stats():
    """Return dataset analytics, SFT count, DPO pairs, and active memory profile."""
    return get_training_dataset_stats()

@router.get("/models")
async def get_models():
    """List registered base and trained model checkpoints."""
    return list_registered_models()

@router.post("/models/select")
async def switch_model(req: SelectModelRequest):
    """Switch active model for chat and inference."""
    ok = set_active_model(req.model_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Model ID not found")
    return {"message": f"Active model switched to {req.model_id}", "model_id": req.model_id}

@router.post("/feedback")
async def submit_feedback(req: FeedbackRequest):
    """
    Captures human feedback (RLHF / DPO) and user corrections during communication.
    Updates in-context learning and feeds the fine-tuning dataset.
    """
    sample = log_conversation_turn(
        prompt=req.prompt,
        response=req.response,
        user_id=req.user_id or "default",
        feedback_rating=req.rating,
        correction=req.correction
    )
    return {
        "status": "logged_for_training",
        "reward_score": sample["reward_score"],
        "sample_id": sample["id"],
        "message": "Feedback integrated into continuous alignment dataset."
    }

@router.post("/jobs")
async def create_fine_tuning_job(req: FineTuneRequest):
    """Start continuous SFT + LoRA fine-tuning job."""
    job = start_fine_tuning_job(
        base_model=req.base_model or "buildwise-llama3-construction-8b",
        epochs=req.epochs or 3,
        learning_rate=req.learning_rate or 0.0002,
        lora_rank=req.lora_rank or 64
    )
    return job

@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    """Get live training telemetry and logs for a job."""
    job = get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/dataset/export")
async def export_dataset(format: str = "openai"):
    """Export dataset in JSONL format for OpenAI, ShareGPT, or Alpaca fine-tuning."""
    return export_training_dataset(format)
