from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from slowapi.util import get_remote_address
from slowapi import Limiter
from app.database import get_db
from app.models import Card
from app.schemas.cards import Card as CardSchema, CardCreate
from app.auth import get_current_user

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

MOCK_CARDS = [
    {"front": "Haben", "back": "Have", "isChecked": False},
    {"front": "Sein", "back": "Be", "isChecked": False},
    {"front": "Werden", "back": "Become", "isChecked": False},
    {"front": "Können", "back": "Can", "isChecked": False},
    {"front": "Müssen", "back": "Must", "isChecked": False},
    {"front": "Sollen", "back": "Should", "isChecked": False},
    {"front": "Wollen", "back": "Want", "isChecked": False},
    {"front": "Dürfen", "back": "May", "isChecked": False},
    {"front": "Machen", "back": "Do/Make", "isChecked": False},
    {"front": "Gehen", "back": "Go", "isChecked": False},
    {"front": "Wissen", "back": "Know", "isChecked": False},
    {"front": "Lesen", "back": "Read", "isChecked": False},
]

@router.get("/", response_model=List[CardSchema])
@limiter.limit("1/minute")
async def get_user_cards(
        request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        result = await db.execute(select(Card).where(Card.user_id == current_user["sub"]))
        cards = result.scalars().all()

        if not cards:
            for mock_card in MOCK_CARDS:
                new_card = Card(
                    user_id=current_user["sub"],
                    front=mock_card["front"],
                    back=mock_card["back"],
                    isChecked=mock_card["isChecked"],
                )
                db.add(new_card)
            await db.commit()
            result = await db.execute(select(Card).where(Card.user_id == current_user["sub"]))
            cards = result.scalars().all()

        return cards
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch cards: {str(e)}")

@router.post("/", response_model=CardSchema)
@limiter.limit("1/minute")
async def add_card(
    request: Request,
    card: CardCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        new_card = Card(
            user_id=current_user["sub"],
            front=card.front,
            back=card.back,
            isChecked=card.isChecked or False,
        )
        db.add(new_card)
        await db.commit()
        await db.refresh(new_card)
        return new_card
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add card: {str(e)}")    

@router.post("/save-checked")
async def save_checked_cards(
    cards: List[CardSchema],
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        for card in cards:
            result = await db.execute(
                select(Card).where(Card.id == card.id, Card.user_id == current_user["sub"])
            )
            db_card = result.scalar_one_or_none()

            if db_card:
                db_card.isChecked = card.isChecked
                db.add(db_card)

        await db.commit()
        return {"message": "Checked cards updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save checked cards: {str(e)}")