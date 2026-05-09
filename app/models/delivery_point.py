import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.database import Base


class DeliveryPoint(Base):
    __tablename__ = "delivery_points"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    zone = Column(String, nullable=True)
    receiver_name = Column(String, nullable=True)
    delivery_schedule = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)