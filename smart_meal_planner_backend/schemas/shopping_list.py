from typing import Optional
from pydantic import BaseModel, Field

class ShoppingListItemBase(BaseModel):
    name: str
    quantity: float = Field(..., gt=0)
    unit: str
    recipe_id: Optional[int] = None

class ShoppingListItemCreate(ShoppingListItemBase):
    pass

class ShoppingListItemUpdate(ShoppingListItemBase):
    name: Optional[str] = None
    quantity: Optional[float] = Field(None, gt=0)
    unit: Optional[str] = None
    purchased: Optional[bool] = None

class ShoppingListItem(ShoppingListItemBase):
    id: int
    purchased: bool

    class Config:
        orm_mode = True 