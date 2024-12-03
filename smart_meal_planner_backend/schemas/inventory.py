from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

class InventoryItemBase(BaseModel):
    name: str
    quantity: float = Field(..., gt=0)
    unit: str
    expiry_date: Optional[date] = None

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemUpdate(InventoryItemBase):
    name: Optional[str] = None
    quantity: Optional[float] = Field(None, gt=0)
    unit: Optional[str] = None

class InventoryItem(InventoryItemBase):
    id: int

    class Config:
        orm_mode = True 