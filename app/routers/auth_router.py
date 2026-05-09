from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_schema import ForgotPasswordRequest, LoginRequest, RegisterRequest
from app.services.auth_service import login_user, register_user, update_user_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    result = login_user(db, data.email, data.password)
    if not result:
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    return result


@router.post("/register", status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    user = register_user(db, data.email, data.password, data.role)
    if not user:
        raise HTTPException(status_code=400, detail="El email ya esta registrado")
    return {"message": "Usuario creado correctamente", "email": user.email, "role": user.role}


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = update_user_password(db, data.email, data.new_password)
    if not user:
        raise HTTPException(status_code=404, detail="No existe un usuario con ese correo")

    return {"message": "Contrasena actualizada correctamente"}
