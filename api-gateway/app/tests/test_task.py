import pytest
import httpx
from app.database import get_db
from sqlalchemy import insert,select,delete
from app.models import User,Task
from sqlalchemy.orm import Session
from app.utils.password import hash_password,verify_password
from app.schemas import AddTaskRequest
from app.tests.test_fixtures import div_session,client
from datetime import datetime, timedelta
import time_machine

@pytest.fixture
def create_new_task_test_sit_up(div_session):
    session=div_session
    test_user= User(
        id=12345689,
        username="TheTest3",
        hashed_password=hash_password("1"),
    )
    session.add(test_user)
    session.commit()
    session.refresh(test_user) 
    currentTime = datetime.now()   

    yield None
    test_users_tasks=session.execute(select(Task).where(Task.user_id==test_user.id)).scalars()
    for task in test_users_tasks:
        session.delete(task)
    session.delete(test_user)
    session.commit()


# using the time_machine to travile will not work in this situatino to test mmarking task as done since the background function is internally for the microservice, we need to test it internally
# I was able to find alternative approach in which i will go back iin the time and then det datetime and asign it to the task
@time_machine.travel(datetime.now()-timedelta(days=10))
@pytest.mark.asyncio
async def test_create_new_task(create_new_task_test_sit_up,client):
    request=AddTaskRequest(
        user_id=12345689,
        title="1",
        description="",
        due_date=datetime.now()
    )
    response=await client.post(
        "http://localhost:8080/tasks/",
        json=request.model_dump(mode="json")
    )
    assert response.status_code ==200
    assert response.json()["title"]=="1"
    assert response.json()["description"]==""
    assert response.json()["status"]=="done"
