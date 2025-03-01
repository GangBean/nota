from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ProjectMember

router = APIRouter()

# 프로젝트 팀원 추가
@router.post("/projects/{project_id}/members", tags=["Teams"], summary="팀원 추가")
def add_team_member(project_id: int, user_id: int, db: Session = Depends(get_db)):
    new_member = ProjectMember(project_id=project_id, user_id=user_id)
    db.add(new_member)
    db.commit()
    return {"message": "User added to project"}

# 프로젝트 팀원 제거
@router.delete("/projects/{project_id}/members/{user_id}", tags=["Teams"], summary="팀원 제거")
def remove_team_member(project_id: int, user_id: int, db: Session = Depends(get_db)):
    member = db.query(ProjectMember).filter(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found in project")

    db.delete(member)
    db.commit()
    return {"message": "User removed from project"}

