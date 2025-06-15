import pytest
import httpx
from app.database import get_db
from sqlalchemy import insert,select,delete
from app.models import User
from sqlalchemy.orm import Session
from app.utils.password import hash_password,verify_password
from app.schemas import LoginRequest


@pytest.fixture
def login_test_sit_up():
    session=next(get_db())
    test_user= User(
        username="TheTest2",
        hashed_password=hash_password("1"),
    )
    session.add(test_user)
    session.commit()
    session.refresh(test_user)        
    (
        yield test_user
    )
    session.delete(test_user)
    session.commit()

@pytest.mark.asyncio
async def test_login(login_test_sit_up):
    try_user=login_test_sit_up
    request=LoginRequest(
        username=try_user.username,
        password="1")
    
    async with httpx.AsyncClient() as client:
        response=await client.post(
            "http://localhost:8000/auth/login",
            json=request.model_dump()
        )

        assert response.status_code ==200