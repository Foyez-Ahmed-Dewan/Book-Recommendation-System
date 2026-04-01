from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.schemas.auth import RegisterRequest, LoginRequest, AuthResponse
from app.core.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return AuthResponse(message="User registered successfully")


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token(user.email)

    return AuthResponse(
        message="Login successful",
        access_token=token,
        token_type="bearer"
    )


@router.get("/profile")
def profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }