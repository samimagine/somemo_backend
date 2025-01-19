from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from ..database import get_db
from ..models import Card
from ..schemas.cards import Card as CardSchema
from ..auth import get_current_user

router = APIRouter()

# Static content for shared general categories
db = {
    "category": "German",
    "title": "Verbs",
    "cards": [
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
    ],
}

# Get all cards for the logged-in user and static content
@router.get("/", response_model=List[CardSchema])
async def get_user_cards(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    # Fetch user-specific cards
    result = await db.execute(select(Card).where(Card.user_id == user["sub"]))
    user_cards = result.scalars().all()

    # Combine user-specific cards with shared static content
    static_cards = [
        CardSchema(**card) for card in db["cards"]
    ]
    return static_cards + user_cards

# Add a new card for the logged-in user
@router.post("/", response_model=CardSchema)
async def add_card(card: CardSchema, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    new_card = Card(**card.dict(), user_id=user["sub"])
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    return new_card

# Update a card for the logged-in user
@router.put("/{card_id}", response_model=CardSchema)
async def update_card(card_id: int, updated_card: CardSchema, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(Card).where(Card.id == card_id, Card.user_id == user["sub"]))
    card_to_update = result.scalar_one_or_none()

    if not card_to_update:
        raise HTTPException(status_code=404, detail="Card not found or not authorized to update")

    for key, value in updated_card.dict(exclude_unset=True).items():
        setattr(card_to_update, key, value)

    db.add(card_to_update)
    await db.commit()
    await db.refresh(card_to_update)
    return card_to_update

# Delete a card for the logged-in user
@router.delete("/{card_id}")
async def delete_card(card_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    result = await db.execute(select(Card).where(Card.id == card_id, Card.user_id == user["sub"]))
    card_to_delete = result.scalar_one_or_none()

    if not card_to_delete:
        raise HTTPException(status_code=404, detail="Card not found or not authorized to delete")

    await db.delete(card_to_delete)
    await db.commit()
    return {"message": "Card deleted successfully"}

# Save the checked status of cards for the logged-in user
@router.post("/save-checked")
async def save_checked_cards(cards: List[CardSchema], db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    for updated_card in cards:
        result = await db.execute(select(Card).where(Card.id == updated_card.id, Card.user_id == user["sub"]))
        card_to_update = result.scalar_one_or_none()

        if card_to_update:
            card_to_update.isChecked = updated_card.isChecked
            db.add(card_to_update)

    await db.commit()
    return {"message": "Checked cards updated successfully"}