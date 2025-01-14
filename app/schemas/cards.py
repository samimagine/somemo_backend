from pydantic import BaseModel
from typing import List

class Card(BaseModel):
    front: str
    back: str

class Deck(BaseModel):
    category: str
    title: str
    cards: List[Card]