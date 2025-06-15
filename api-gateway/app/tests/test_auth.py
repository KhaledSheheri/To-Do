import pytest
import httpx
from app.database import get_db
from sqlalchemy import insert,select,delete
from app.models import User
from sqlalchemy.orm import Session
from app.utils.password import hash_password,verify_password
from app.schemas import LoginRequest
from app.tests.test_fixtures import div_session,client


@pytest.fixture
def login_test_sit_up(div_session):
    session=div_session
    test_user= User(
        username="TheTest2",
        hashed_password=hash_password("1"),
    )
    session.add(test_user)
    session.commit()
    session.refresh(test_user)        
    
    yield None
    
    session.delete(test_user)
    session.commit()

@pytest.mark.asyncio
async def test_login(login_test_sit_up,client):

    
    request=LoginRequest(
        username="TheTest2",
        password="1")
    
    response=await client.post(
        "http://localhost:8000/auth/login",
        json=request.model_dump()
    )

    assert response.status_code ==200
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "bearer"
    