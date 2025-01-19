from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel

class Card(BaseModel):
    id: Optional[int]  # For database ID
    user_id: Optional[int]  # ID of the user who owns the card
    front: str
    back: str
    isChecked: Optional[bool] = False

    class Config:
        orm_mode = True

class Deck(BaseModel):
    category: str
    title: str
    cards: List[Card]