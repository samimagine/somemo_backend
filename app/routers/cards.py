from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models import Card
from app.schemas.cards import Card as CardSchema
from app.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CardSchema])
async def get_user_cards(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        result = await db.execute(select(Card).where(Card.user_id == current_user["sub"]))
        cards = result.scalars().all()
        return cards
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch cards")

@router.post("/", response_model=CardSchema)
async def add_card(
    card: CardSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    new_card = Card(**card.dict(), user_id=current_user["sub"])
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    return new_card