from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from slowapi.util import get_remote_address
from slowapi import Limiter
from app.database import get_db
from app.models import User
from app.schemas.auth import UserCreate, UserResponse, LoginRequest, Token
from app.auth import hash_password, verify_password, create_access_token

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.post("/register", response_model=UserResponse)
@limiter.limit("3/minute")
async def register(
    request: Request,
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        hashed_password=hashed_password,
        is_admin=user.is_admin,
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request,
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.username == data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(data={"sub": user.id})
    print(f"Token created for User ID {user.id}: {access_token}")
    return {"access_token": access_token, "token_type": "bearer"}