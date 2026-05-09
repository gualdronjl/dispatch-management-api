from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.delivery_point import DeliveryPoint
from app.schemas.delivery_schema import DeliveryPointCreate, DeliveryPointUpdate, DeliveryPointResponse
from app.utils.security import get_current_user, require_role

router = APIRouter(prefix="/delivery-points", tags=["DeliveryPoints"])


@router.post("/", response_model=DeliveryPointResponse)
def create(data: DeliveryPointCreate, db: Session = Depends(get_db),
           current_user=Depends(require_role("ADMIN", "OPERADOR"))):
    point = DeliveryPoint(**data.model_dump())
    db.add(point)
    db.commit()
    db.refresh(point)
    return point


@router.get("/", response_model=list[DeliveryPointResponse])
def list_all(db: Session = Depends(get_db),
             current_user=Depends(get_current_user)):
    return db.query(DeliveryPoint).all()


@router.get("/{point_id}", response_model=DeliveryPointResponse)
def get_one(point_id: UUID, db: Session = Depends(get_db),
            current_user=Depends(get_current_user)):
    point = db.query(DeliveryPoint).filter(DeliveryPoint.id == point_id).first()
    if not point:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Punto de entrega no encontrado")
    return point


@router.put("/{point_id}", response_model=DeliveryPointResponse)
def update(point_id: UUID, data: DeliveryPointUpdate, db: Session = Depends(get_db),
           current_user=Depends(require_role("ADMIN", "OPERADOR"))):
    point = db.query(DeliveryPoint).filter(DeliveryPoint.id == point_id).first()
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(point, field, value)
    db.commit()
    db.refresh(point)
    return point


@router.delete("/{point_id}")
def delete(point_id: UUID, db: Session = Depends(get_db),
           current_user=Depends(require_role("ADMIN"))):
    point = db.query(DeliveryPoint).filter(DeliveryPoint.id == point_id).first()
    db.delete(point)
    db.commit()
    return {"message": "Punto de entrega eliminado"}