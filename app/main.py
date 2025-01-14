from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .database import Base, engine, get_db
from .models import User
from .schemas import UserCreate, UserResponse, Token
from .auth import hash_password, verify_password, create_access_token, decode_token
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password, is_admin=user.is_admin)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")

@app.post("/login", response_model=Token)
async def login(username: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username, "is_admin": user.is_admin})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected-route")
async def protected_route(token: str = Depends(decode_token)):
    return {"message": "This is a protected route", "user": token}