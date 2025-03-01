from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# 다대다 관계 테이블
role_api_permission = Table(
    "role_api_permission",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("api_permission_id", Integer, ForeignKey("api_permissions.id"))
)

tenant_project = Table(
    "tenant_project",
    Base.metadata,
    Column("tenant_id", Integer, ForeignKey("tenants.id")),
    Column("project_id", Integer, ForeignKey("projects.id"))
)

# 테넌트(조직)
class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

# 사용자
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))

    tenant = relationship("Tenant")
    role = relationship("Role")

# 역할(Role)
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

# API 권한
class ApiPermission(Base):
    __tablename__ = "api_permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    endpoint = Column(String)
    method = Column(String)

# 프로젝트
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")

# 프로젝트 멤버
class ProjectMember(Base):
    __tablename__ = "project_members"

    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

