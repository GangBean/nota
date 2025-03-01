from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserLogin, UserResponse
from models import User
from auth import create_access_token, hash_password, verify_password

router = APIRouter()

# 회원가입 (이메일 인증 포함)
@router.post("/users", response_model=UserResponse, tags=["Users"], summary="회원가입")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, password=hashed_password, tenant_id=user.tenant_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 이메일 인증 코드 확인
@router.post("/users/email-verifications", tags=["Users"], summary="이메일 인증 확인")
def verify_email(email: str, code: str, db: Session = Depends(get_db)):
    # 이메일 인증 로직 추가
    return {"message": "Email verified"}

# 로그인 (JWT 발급)
@router.post("/auth/tokens", tags=["Users"], summary="로그인")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(db_user.id)
    return {"access_token": token}

# 비밀번호 재설정 요청 (이메일 발송)
@router.post("/users/password-reset-requests", tags=["Users"], summary="비밀번호 재설정 요청")
def request_password_reset(email: str, db: Session = Depends(get_db)):
    # 비밀번호 재설정 이메일 발송 로직 추가
    return {"message": "Password reset email sent"}

# 비밀번호 재설정
@router.post("/users/passwords", tags=["Users"], summary="비밀번호 재설정")
def reset_password(email: str, new_password: str, db: Session = Depends(get_db)):
    # 비밀번호 변경 로직 추가
    return {"message": "Password has been reset"}
