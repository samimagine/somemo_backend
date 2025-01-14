from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas.cards import Card, Deck

router = APIRouter()

db = {
    "category": "German",
    "title": "Verbs",
    "cards": [
        {"front": "Haben", "back": "Have"},
        {"front": "Sein", "back": "Be"},
        {"front": "Werden", "back": "Become"},
        {"front": "Können", "back": "Can"},
        {"front": "Müssen", "back": "Must"},
        {"front": "Sollen", "back": "Should"},
        {"front": "Wollen", "back": "Want"},
        {"front": "Dürfen", "back": "May"},
        {"front": "Machen", "back": "Do/Make"},
        {"front": "Gehen", "back": "Go"},
        {"front": "Wissen", "back": "Know"},
        {"front": "Lesen", "back": "Read"},
    ],
}

@router.get("/", response_model=Deck)
def get_cards():
    return db

@router.post("/", response_model=Card)
def add_card(card: Card):
    db["cards"].append(card.dict())
    return card

@router.put("/{card_index}", response_model=Card)
def update_card(card_index: int, card: Card):
    try:
        db["cards"][card_index] = card.dict()
        return card
    except IndexError:
        raise HTTPException(status_code=404, detail="Card not found")

@router.delete("/{card_index}")
def delete_card(card_index: int):
    try:
        removed_card = db["cards"].pop(card_index)
        return {"message": "Card removed", "card": removed_card}
    except IndexError:
        raise HTTPException(status_code=404, detail="Card not found")