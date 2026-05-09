from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import verify_password, create_access_token, hash_password


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None

    token = create_access_token({
        "user_id": str(user.id),
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat()
        }
    }


def register_user(db: Session, email: str, password: str, role: str = "OPERATOR"):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return None
    user = User(
        email=email,
        password_hash=hash_password(password),
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user