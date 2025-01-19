from pydantic import BaseModel
from typing import Optional, List

class Card(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    front: str
    back: str
    isChecked: Optional[bool] = False

    class Config:
        orm_mode = True

class Deck(BaseModel):
    category: str
    title: str
    cards: List[Card]