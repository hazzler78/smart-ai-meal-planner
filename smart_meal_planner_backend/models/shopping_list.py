from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class ShoppingListItem(Base):
    __tablename__ = "shopping_list"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Float)
    unit = Column(String)
    purchased = Column(Boolean, default=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)

    recipe = relationship("Recipe", back_populates="shopping_list_items")

    class Config:
        orm_mode = True 