from sqlalchemy import Column, Integer, String, JSON, DateTime, CheckConstraint, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    ingredients = Column(JSON, nullable=False)  # [{"name": "flour", "quantity": 200, "unit": "g"}]
    instructions = Column(JSON, nullable=False)  # ["Step 1", "Step 2", ...]
    prep_time = Column(Integer, nullable=False, default=0)
    cook_time = Column(Integer, nullable=False, default=0)
    servings = Column(Integer, nullable=False, default=1)
    tags = Column(JSON, nullable=True, default=list)  # ["vegan", "quick", "gluten-free"]
    rating = Column(Float, nullable=True)  # Optional rating field (0-5)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    __table_args__ = (
        CheckConstraint('prep_time >= 0', name='check_prep_time_positive'),
        CheckConstraint('cook_time >= 0', name='check_cook_time_positive'),
        CheckConstraint('servings > 0', name='check_servings_positive'),
        CheckConstraint('rating >= 0 AND rating <= 5', name='check_rating_range'),
    )

    # Relationship with shopping list items
    shopping_list_items = relationship(
        "ShoppingListItem",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Recipe(id={self.id}, name='{self.name}', prep_time={self.prep_time}, cook_time={self.cook_time})>"

    class Config:
        orm_mode = True 