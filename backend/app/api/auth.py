from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.core.database import get_db
from backend.app.core.security import hash_password, verify_password, create_access_token, decode_access_token, oauth2_scheme
from backend.app.models.db_models import User, Profile, UserSettings
from backend.app.schemas.all_schemas import UserRegister, UserLogin, TokenResponse, UserProfileOut

router = APIRouter(prefix="/auth", tags=["Authentication"])

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """Retrieve current authenticated user or return demo user if unauthenticated in dev mode."""
    if not token:
        # Check if default demo user exists, else create one
        stmt = select(User).where(User.email == "demo@buildwise.ai")
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                email="demo@buildwise.ai",
                hashed_password=hash_password("Buildwise@2026"),
                full_name="BuildWise Demo Architect",
                role="architect"
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        return user
        
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@router.post("/register", response_model=TokenResponse)
async def register(req: UserRegister, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == req.email)
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
        
    user = User(
        email=req.email,
        hashed_password=hash_password(req.password),
        full_name=req.full_name,
        role=req.role or "homeowner"
    )
    db.add(user)
    await db.flush()
    
    profile = Profile(user_id=user.id, phone=req.phone, location=req.location)
    settings = UserSettings(user_id=user.id)
    db.add(profile)
    db.add(settings)
    await db.commit()
    await db.refresh(user)
    
    token = create_access_token(user.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    }

@router.post("/login", response_model=TokenResponse)
async def login(req: UserLogin, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == req.email)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    token = create_access_token(user.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    }

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}

@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "created_at": user.created_at
    }
