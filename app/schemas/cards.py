from pydantic import BaseModel
from typing import Optional

class CardBase(BaseModel):
    front: str
    back: str
    isChecked: Optional[bool] = False

class CardCreate(CardBase):
    pass  # This schema is used for incoming requests and does not include id or user_id

class Card(CardBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True