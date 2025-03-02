from pydantic import BaseModel, EmailStr
from typing import Optional, List

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

# 프로젝트 수정 스키마 (PATCH 요청 처리)
class ProjectUpdate(BaseModel):
    name: Optional[str] = None  # 프로젝트 이름 수정 가능
    owner_id: Optional[int] = None  # 프로젝트 소유자 변경 가능

# 역할 생성 스키마 추가
class RoleCreate(BaseModel):
    name: str  # 역할 이름 필수

class ApiPermissionResponse(BaseModel):
    id: int
    name: str
    endpoint: str
    method: str

class RoleResponse(BaseModel):
    id: int
    name: str
    permissions: List[ApiPermissionResponse]  # 역할별 API 권한 포함
