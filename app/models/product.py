import uuid
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sku = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    unit = Column(String, nullable=False)
    status = Column(String, default="ACTIVE")  # ACTIVE | INACTIVE
    created_at = Column(DateTime, default=datetime.utcnow)