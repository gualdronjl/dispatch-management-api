import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Dispatch(Base):
    __tablename__ = "dispatches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    delivery_point_id = Column(UUID(as_uuid=True), ForeignKey("delivery_points.id"), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    dispatch_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="PENDIENTE")  # PENDIENTE | ENVIADO | ENTREGADO | CANCELADO
    created_at = Column(DateTime, default=datetime.utcnow)

    delivery_point = relationship("DeliveryPoint", backref="dispatches")
    created_by_user = relationship("User", backref="dispatches")
    details = relationship("DispatchDetail", back_populates="dispatch", cascade="all, delete")