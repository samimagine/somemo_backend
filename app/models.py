from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)

    cards = relationship("Card", back_populates="user")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)  # Auto-generated
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Backend assigns this
    front = Column(String, nullable=False)  # Required
    back = Column(String, nullable=False)  # Required
    isChecked = Column(Boolean, default=False)  # Defaults to False

    user = relationship("User", back_populates="cards")