from fastapi import FastAPI, HTTPException
from typing import List, Dict
from pydantic import BaseModel

app = FastAPI()

# In-memory database
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
        {"front": "Lesen", "back": "Read"}
    ]
}

# Models
class Card(BaseModel):
    front: str
    back: str

class Deck(BaseModel):
    category: str
    title: str
    cards: List[Card]

# Get all cards
@app.get("/cards", response_model=Deck)
def get_cards():
    return db

# Add a card
@app.post("/cards", response_model=Card)
def add_card(card: Card):
    db["cards"].append(card.dict())
    return card

# Update a card
@app.put("/cards/{card_index}", response_model=Card)
def update_card(card_index: int, card: Card):
    try:
        db["cards"][card_index] = card.dict()
        return card
    except IndexError:
        raise HTTPException(status_code=404, detail="Card not found")

# Delete a card
@app.delete("/cards/{card_index}")
def delete_card(card_index: int):
    try:
        removed_card = db["cards"].pop(card_index)
        return {"message": "Card removed", "card": removed_card}
    except IndexError:
        raise HTTPException(status_code=404, detail="Card not found")