from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class ProductCreate(BaseModel):
    sku: str
    name: str
    stock: int
    unit: str


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    stock: Optional[int] = None
    unit: Optional[str] = None
    status: Optional[str] = None


class ProductResponse(BaseModel):
    id: UUID
    sku: str
    name: str
    stock: int
    unit: str
    status: str

    class Config:
        from_attributes = True