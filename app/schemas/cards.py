from pydantic import BaseModel
from typing import Optional, List

class Card(BaseModel):
    id: Optional[int]  # Backend generates this
    user_id: Optional[int]  # Automatically assigned based on the logged-in user
    front: str  # Required
    back: str  # Required
    isChecked: Optional[bool] = False  # Defaults to False

    class Config:
        orm_mode = True

class Deck(BaseModel):
    category: str
    title: str
    cards: List[Card]