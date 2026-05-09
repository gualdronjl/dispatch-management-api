from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional
from datetime import datetime


class DispatchDetailCreate(BaseModel):
    product_id: UUID
    quantity: int


class DispatchCreate(BaseModel):
    delivery_point_id: UUID
    details: List[DispatchDetailCreate]


class DispatchStatusUpdate(BaseModel):
    status: str  # PENDIENTE | ENVIADO | ENTREGADO | CANCELADO


class DispatchDetailResponse(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int

    class Config:
        from_attributes = True


class DispatchResponse(BaseModel):
    id: UUID
    delivery_point_id: UUID
    created_by: UUID
    status: str
    dispatch_date: datetime
    details: List[DispatchDetailResponse] = []

    class Config:
        from_attributes = True