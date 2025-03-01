from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from api import users, projects, roles, teams
from database import engine, Base, SessionLocal
from fastapi.openapi.utils import get_openapi
import models

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI 서버가 시작되었습니다.")
    
    # 데이터베이스 초기화 (기본 테넌트 확인 및 생성)
    db = SessionLocal()
    if not db.query(models.Tenant).filter(models.Tenant.id == 0).first():
        db.add(models.Tenant(id=0, name="Default Tenant"))
        db.commit()
        print("기본 테넌트가 생성되었습니다.")
    db.close()

    yield  # 앱 실행 중

    print("FastAPI 서버가 종료됩니다.")

app = FastAPI(
    title="Nota API",
    description="Nota Project API 문서",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
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
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(teams.router, prefix="/teams", tags=["Teams"])
app.include_router(roles.router, prefix="/roles", tags=["Roles"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Nota API"}
