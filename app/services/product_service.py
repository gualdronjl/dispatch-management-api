from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product


def create_product(db: Session, data):
    existing = db.query(Product).filter(Product.sku == data.sku).first()
    if existing:
        raise HTTPException(status_code=400, detail="SKU ya registrado")
    product = Product(
        sku=data.sku,
        name=data.name,
        stock=data.stock,
        unit=data.unit
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(db: Session):
    return db.query(Product).filter(Product.status == "ACTIVE").all()


def get_product(db: Session, product_id: UUID):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product


def update_product(db: Session, product_id: UUID, data):
    product = get_product(db, product_id)
    print("product ", product)
    print("data ", data)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: UUID):
    product = get_product(db, product_id)
    product.status = "INACTIVE"
    db.commit()
    return {"message": "Producto desactivado"}