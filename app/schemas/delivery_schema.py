from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class DeliveryPointCreate(BaseModel):
    name: str
    address: str
    city: str
    zone: Optional[str] = None
    receiver_name: Optional[str] = None
    delivery_schedule: Optional[str] = None


class DeliveryPointUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    zone: Optional[str] = None
    receiver_name: Optional[str] = None
    delivery_schedule: Optional[str] = None


class DeliveryPointResponse(BaseModel):
    id: UUID
    name: str
    address: str
    city: str
    zone: Optional[str] = None
    receiver_name: Optional[str] = None
    delivery_schedule: Optional[str] = None

    class Config:
        from_attributes = True