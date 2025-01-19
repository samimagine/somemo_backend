from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models import Card
from app.schemas.cards import Card as CardSchema
from app.auth import get_current_user

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
async def get_user_cards(
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
        raise HTTPException(status_code=500, detail="Failed to fetch cards")

@router.post("/", response_model=CardSchema)
async def add_card(
    card: CardSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        new_card = Card(**card.dict(), user_id=current_user["sub"])
        db.add(new_card)
        await db.commit()
        await db.refresh(new_card)
        return new_card
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to add card")