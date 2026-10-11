from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Dict, Any, Optional
from backend.app.core.database import get_db
from backend.app.api.auth import get_current_user
from backend.app.models.db_models import User, Conversation, Message
from backend.app.schemas.all_schemas import ChatMessageRequest
from backend.app.services.llm_service import generate_chat_response, stream_chat_response

router = APIRouter(tags=["Chat"])

@router.get("/conversations")
async def list_conversations(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Conversation).where(Conversation.user_id == user.id).order_by(Conversation.updated_at.desc())
    res = await db.execute(stmt)
    convs = res.scalars().all()
    return [
        {
            "id": c.id,
            "title": c.title,
            "project_id": c.project_id,
            "pinned": c.pinned,
            "created_at": c.created_at,
            "updated_at": c.updated_at
        }
        for c in convs
    ]

@router.post("/conversations")
async def create_conversation(
    payload: Dict[str, Any],
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    title = payload.get("title", "New Construction Consultation")
    project_id = payload.get("project_id")
    conv = Conversation(user_id=user.id, title=title, project_id=project_id)
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return {
        "id": conv.id,
        "title": conv.title,
        "project_id": conv.project_id,
        "created_at": conv.created_at
    }

@router.get("/conversations/{id}")
async def get_conversation(
    id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Conversation).where(Conversation.id == id, Conversation.user_id == user.id)
    res = await db.execute(stmt)
    conv = res.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    msg_stmt = select(Message).where(Message.conversation_id == id).order_by(Message.created_at.asc())
    msg_res = await db.execute(msg_stmt)
    messages = msg_res.scalars().all()
    
    return {
        "id": conv.id,
        "title": conv.title,
        "project_id": conv.project_id,
        "created_at": conv.created_at,
        "messages": [
            {
                "id": m.id,
                "sender": m.sender,
                "content": m.content,
                "model_used": m.model_used,
                "structured_data": m.structured_data,
                "tool_calls": m.tool_calls,
                "created_at": m.created_at
            }
            for m in messages
        ]
    }

@router.patch("/conversations/{id}")
async def update_conversation(
    id: str,
    payload: Dict[str, Any],
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Conversation).where(Conversation.id == id, Conversation.user_id == user.id)
    res = await db.execute(stmt)
    conv = res.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    if "title" in payload:
        conv.title = payload["title"]
    if "pinned" in payload:
        conv.pinned = payload["pinned"]
    await db.commit()
    return {"message": "Updated successfully"}

@router.delete("/conversations/{id}")
async def delete_conversation(
    id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Conversation).where(Conversation.id == id, Conversation.user_id == user.id)
    res = await db.execute(stmt)
    conv = res.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await db.delete(conv)
    await db.commit()
    return {"message": "Deleted successfully"}

@router.post("/chat")
async def chat_endpoint(
    req: ChatMessageRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Ensure conversation
    conv_id = req.conversation_id
    if not conv_id:
        conv = Conversation(user_id=user.id, title=req.message[:35] + ("..." if len(req.message) > 35 else ""))
        db.add(conv)
        await db.flush()
        conv_id = conv.id
    
    # Load previous conversation history
    msg_stmt = select(Message).where(Message.conversation_id == conv_id).order_by(Message.created_at.asc())
    msg_res = await db.execute(msg_stmt)
    history = [{"role": m.sender, "content": m.content} for m in msg_res.scalars().all()]
    history.append({"role": "user", "content": req.message})

    # Save user message
    user_msg = Message(
        conversation_id=conv_id,
        sender="user",
        content=req.message
    )
    db.add(user_msg)

    # Generate response
    ai_res = await generate_chat_response(messages=history, model_name=req.model)

    # Save assistant message
    asst_msg = Message(
        conversation_id=conv_id,
        sender="assistant",
        content=ai_res["content"],
        model_used=req.model,
        tool_calls=ai_res["tool_calls"],
        structured_data=ai_res["structured_data"]
    )
    db.add(asst_msg)
    await db.commit()
    await db.refresh(asst_msg)
    
    return {
        "conversation_id": conv_id,
        "message": {
            "id": asst_msg.id,
            "sender": asst_msg.sender,
            "content": asst_msg.content,
            "tool_calls": asst_msg.tool_calls,
            "structured_data": asst_msg.structured_data,
            "created_at": asst_msg.created_at
        }
    }

@router.post("/chat/stream")
async def chat_stream_endpoint(
    req: ChatMessageRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Server-Sent Events endpoint streaming tokens and final tool results."""
    # Ensure conversation
    conv_id = req.conversation_id
    if not conv_id:
        conv = Conversation(user_id=user.id, title=req.message[:35])
        db.add(conv)
        await db.flush()
        conv_id = conv.id
        
    user_msg = Message(conversation_id=conv_id, sender="user", content=req.message)
    db.add(user_msg)
    await db.commit()
    
    history = [{"role": "user", "content": req.message}]
    
    return StreamingResponse(
        stream_chat_response(messages=history, model_name=req.model),
        media_type="text/event-stream"
    )
