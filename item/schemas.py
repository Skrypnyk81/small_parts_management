from pydantic import BaseModel
from datetime import datetime

class ItemCreate(BaseModel):
    name: str
    description: str 
    quantity: int
    minimum_quantity: int

class Item(BaseModel):
    id: int
    name: str
    description: str
    quantity: int
    minimum_quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
