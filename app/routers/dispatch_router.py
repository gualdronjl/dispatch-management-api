from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.dispatch_schema import DispatchCreate, DispatchStatusUpdate, DispatchResponse
from app.services.dispatch_service import (
    create_dispatch, get_dispatches, get_dispatch, update_dispatch_status
)
from app.utils.security import get_current_user, require_role

router = APIRouter(prefix="/dispatches", tags=["Dispatches"])


@router.post("/", response_model=DispatchResponse)
def create(data: DispatchCreate, db: Session = Depends(get_db),
           current_user=Depends(require_role("ADMIN", "OPERADOR"))):
    return create_dispatch(db, data, current_user)


@router.get("/", response_model=list[DispatchResponse])
def list_all(status: Optional[str] = None, db: Session = Depends(get_db),
             current_user=Depends(get_current_user)):
    return get_dispatches(db, status)


@router.get("/{dispatch_id}", response_model=DispatchResponse)
def get_one(dispatch_id: UUID, db: Session = Depends(get_db),
            current_user=Depends(get_current_user)):
    return get_dispatch(db, dispatch_id)


@router.patch("/{dispatch_id}/status", response_model=DispatchResponse)
def change_status(dispatch_id: UUID, data: DispatchStatusUpdate,
                  db: Session = Depends(get_db),
                  current_user=Depends(require_role("ADMIN", "OPERADOR", "SUPERVISOR"))):
    return update_dispatch_status(db, dispatch_id, data.status, current_user)