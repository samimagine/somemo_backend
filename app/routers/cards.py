from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas.cards import Card, Deck

router = APIRouter()

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

@router.post("/save-checked")
def save_checked_cards(cards: List[Card]):
    for updated_card in cards:
        for existing_card in db["cards"]:
            if existing_card["front"] == updated_card.front and existing_card["back"] == updated_card.back:
                existing_card["isChecked"] = updated_card.isChecked
    return {"message": "Checked cards updated successfully", "updatedCards": cards}