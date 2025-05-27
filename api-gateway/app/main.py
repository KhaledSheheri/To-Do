from fastapi import FastAPI
from app.routes import auth_proxy, tasks_proxy,share_proxy
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models


app = FastAPI(title="API Gateway")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], ## to limit the access to be only from the Application Public Gateway
    allow_credentials=True,
    ##allow_methods=["*"],
    ##allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_proxy.router, prefix="/auth", tags=["Auth"])
app.include_router(tasks_proxy.router, prefix="/tasks", tags=["Tasks"])
app.include_router(share_proxy.router, prefix="/taskshare", tags=["TaskShare"])


@app.get("/")
def health_check():
    return {"status": "API Gateway is running"}

from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="API Gateway",
        version="0.1.0",
        description="Your API Gateway",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi