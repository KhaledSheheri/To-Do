from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import User
from app.schemas import RegisterRequest, UserResponse, RegisterResponse,LoginResponse,LoginRequest
from app.utils.password import hash_password,verify_password
from app.utils.jwt_handler import create_access_token


def register_user(db: Session, payload: RegisterRequest) -> RegisterResponse:
    existing_user = db.query(User).filter(
        (User.username == payload.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User Exist"
        )
    
    hashedPassword=hash_password(payload.passward)
    new_user= User(
        username=payload.username,
        hashed_password=hashedPassword,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RegisterResponse(
        statusCode=status.HTTP_201_CREATED,
        message="User created successfully"
    )

def login_user(db: Session, payload: LoginRequest) -> LoginResponse:
    user = db.query(User).filter(User.username == payload.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )
    
    token = create_access_token(data={"id": user.id, "username": user.username})

    return LoginResponse(access_token=token)

