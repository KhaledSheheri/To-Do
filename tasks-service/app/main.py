from fastapi import FastAPI
from app.routes import tasks_router
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models


app=FastAPI(
    title="Tasks Microservice",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], ## to limit the access to be only from the Application Public Gateway
    allow_credentials=True,
    ##allow_methods=["*"],
    ##allow_headers=["*"],
)

Base.metadata.create_all(engine)

app.include_router(tasks_router.router,prefix="/tasks",tags=["Tasks"])

@app.get("/")
def health_check():
    return {"status": "Authentication service is running"}
