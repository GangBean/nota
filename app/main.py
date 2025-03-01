from fastapi import FastAPI
from api import users, projects, auth
from database import engine, Base

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

# API 라우트 추가
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Nota API"}

