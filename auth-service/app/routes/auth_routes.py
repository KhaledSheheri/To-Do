from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import RegisterRequest, LoginRequest, UserResponse, LoginResponse, RegisterResponse ,TokenData
from app.services.auth_service import register_user , login_user
from app.services.token_service import get_current_user,verify_token



router=APIRouter()

@router.get("/me")
def get_current_user(user = Depends(get_current_user)):
    return user

@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(db,payload)

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, payload)

@router.post("/verify")
def verify(data: TokenData):
    return verify_token(data)