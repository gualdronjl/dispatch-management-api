from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.dispatch import Dispatch
from app.models.dispatch_detail import DispatchDetail
from app.models.product import Product

VALID_TRANSITIONS = {
    "PENDIENTE": ["ENVIADO", "CANCELADO"],
    "ENVIADO": ["ENTREGADO", "CANCELADO"],
    "ENTREGADO": [],
    "CANCELADO": [],
}


def create_dispatch(db: Session, data, current_user):
    dispatch = Dispatch(
        delivery_point_id=data.delivery_point_id,
        created_by=current_user.id,
        status="PENDIENTE"
    )
    db.add(dispatch)
    db.flush()

    for item in data.details:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto {item.product_id} no existe")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {product.name}")
        product.stock -= item.quantity
        detail = DispatchDetail(
            dispatch_id=dispatch.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(detail)

    db.commit()
    db.refresh(dispatch)
    return dispatch


def get_dispatches(db: Session, status: str = None):
    query = db.query(Dispatch)
    if status:
        query = query.filter(Dispatch.status == status.upper())
    return query.all()


def get_dispatch(db: Session, dispatch_id: UUID):
    dispatch = db.query(Dispatch).filter(Dispatch.id == dispatch_id).first()
    if not dispatch:
        raise HTTPException(status_code=404, detail="Despacho no encontrado")
    return dispatch


def update_dispatch_status(db: Session, dispatch_id: UUID, new_status: str, current_user):
    dispatch = get_dispatch(db, dispatch_id)
    new_status = new_status.upper()
    allowed = VALID_TRANSITIONS.get(dispatch.status, [])
    if new_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"No se puede cambiar de {dispatch.status} a {new_status}"
        )
    dispatch.status = new_status
    db.commit()
    db.refresh(dispatch)
    return dispatch