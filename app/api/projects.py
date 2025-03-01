from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Project
from schemas import ProjectCreate, ProjectUpdate

router = APIRouter()

# 프로젝트 생성
@router.post("/projects", tags=["Projects"], summary="프로젝트 생성")
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Project(name=project.name, owner_id=project.owner_id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# 프로젝트 전체 조회
@router.get("/projects", tags=["Projects"], summary="프로젝트 전체 조회")
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

# 프로젝트 상세 조회
@router.get("/projects/{project_id}", tags=["Projects"], summary="프로젝트 상세 조회")
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# 프로젝트 수정 (소유자만 가능)
@router.patch("/projects/{project_id}", tags=["Projects"], summary="프로젝트 수정")
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in project.dict(exclude_unset=True).items():
        setattr(db_project, key, value)

    db.commit()
    return db_project

# 프로젝트 삭제 (소유자만 가능)
@router.delete("/projects/{project_id}", tags=["Projects"], summary="프로젝트 삭제")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}
