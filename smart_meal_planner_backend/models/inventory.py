from sqlalchemy import Column, Integer, String, Float, Date
from ..database import Base

class InventoryItem(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Float)
    unit = Column(String)
    expiry_date = Column(Date)

    class Config:
        orm_mode = True 