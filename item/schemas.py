from fastapi import Form
from pydantic import BaseModel
from datetime import datetime
from typing import Annotated


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


class ItemAdd(BaseModel):
    name: str
    description: str
    quantity: int

    @classmethod
    def as_form(
        cls,
        name: Annotated[str, Form()],
        description: Annotated[str, Form()],
        quantity: Annotated[int, Form()]
    ):
        return cls(name=name, description=description, quantity=quantity)
