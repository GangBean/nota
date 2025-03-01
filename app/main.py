from fastapi import FastAPI
from api import users, projects, auth
from database import engine, Base
from fastapi.openapi.utils import get_openapi

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nota API",
    description="Nota Project API 문서",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Nota API",
        version="1.0.0",
        description="Nota Project API 문서",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# API 라우트 추가
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Nota API"}

