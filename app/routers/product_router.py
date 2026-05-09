from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import (
    create_product, get_products, get_product, update_product, delete_product
)
from app.utils.security import get_current_user, require_role

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse)
def create(data: ProductCreate, db: Session = Depends(get_db),
           current_user=Depends(require_role("ADMIN", "OPERADOR"))):
    return create_product(db, data)


@router.get("/", response_model=list[ProductResponse])
def list_all(db: Session = Depends(get_db),
             current_user=Depends(get_current_user)):
    return get_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_one(product_id: UUID, db: Session = Depends(get_db),
            current_user=Depends(get_current_user)):
    return get_product(db, product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update(product_id: UUID, data: ProductUpdate, db: Session = Depends(get_db),
           current_user=Depends(require_role("ADMIN", "OPERADOR"))):
    return update_product(db, product_id, data)


@router.delete("/{product_id}")
def delete(product_id: UUID, db: Session = Depends(get_db),
           current_user=Depends(require_role("ADMIN"))):
    return delete_product(db, product_id)