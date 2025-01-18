from pydantic import BaseModel
from typing import List, Optional

class Card(BaseModel):
    front: str
    back: str
    isChecked: Optional[bool] = False

class Deck(BaseModel):
    category: str
    title: str
    cards: List[Card]