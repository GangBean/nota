from pydantic import BaseModel, EmailStr
from typing import Optional

# 사용자 스키마
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    tenant_id: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    tenant_id: int

    class Config:
        orm_mode = True

# 프로젝트 스키마
class ProjectCreate(BaseModel):
    name: str
    owner_id: int

class ProjectResponse(BaseModel):
    id: int
    name: str
    owner_id: int

    class Config:
        orm_mode = True

