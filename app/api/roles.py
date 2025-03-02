from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Role, ApiPermission
from schemas import RoleCreate, RoleResponse

router = APIRouter()

# 역할 목록 조회
@router.get("/roles", response_model=list[RoleResponse], tags=["Roles"], summary="역할 목록 조회")
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).options(joinedload(Role.permissions)).all()  # ✅ JOIN 활용
    
    return roles

# 새로운 역할 생성 (관리자)
@router.post("/roles", tags=["Roles"], summary="새로운 역할 생성")
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    new_role = Role(name=role.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

# 역할에 API 권한 추가
@router.post("/roles/{role_id}/permissions", tags=["Roles"], summary="역할에 API 권한 추가")
def add_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    permission = db.query(ApiPermission).filter(ApiPermission.id == permission_id).first()
    if not role or not permission:
        raise HTTPException(status_code=404, detail="Role or Permission not found")

    role.permissions.append(permission)
    db.commit()
    return {"message": "Permission added to role"}

# 역할에서 API 권한 제거
@router.delete("/roles/{role_id}/permissions/{permission_id}", tags=["Roles"], summary="역할에서 API 권한 제거")
def remove_permission_from_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    permission = db.query(ApiPermission).filter(ApiPermission.id == permission_id).first()
    if not role or not permission:
        raise HTTPException(status_code=404, detail="Role or Permission not found")

    role.permissions.remove(permission)
    db.commit()
    return {"message": "Permission removed from role"}

