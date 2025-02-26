# nota
nota backend engineer position assignment project

# ERD
```mermaid
erDiagram

    %% 사용자 테이블
    USER {
        int id PK
        int tenant_id FK
        string email
        string password
        int role_id FK
    }

    %% 역할 테이블
    ROLE {
        int id PK
        string name
    }

    %% API 권한 테이블
    API_PERMISSION {
        int id PK
        string name
        string endpoint
        string method
    }

    %% 역할-API 권한 연결 테이블 (다대다 관계 해결)
    ROLE_API_PERMISSION {
        int role_id FK
        int api_permission_id FK
    }

    %% 테넌트(조직) 테이블
    TENANT {
        int id PK
        string name
    }

    %% 프로젝트 테이블
    PROJECT {
        int id PK
        string name
        int owner_id FK
    }

    %% 테넌트-프로젝트 다대다 관계 해결 테이블
    TENANT_PROJECT {
        int tenant_id FK
        int project_id FK
    }

    %% 프로젝트 팀원 테이블 (role_id 제거)
    PROJECT_MEMBER {
        int project_id FK
        int user_id FK
    }

    %% 관계 설정
    USER ||--|| TENANT : belongs_to
    USER ||--|| ROLE : has
    ROLE ||--o{ ROLE_API_PERMISSION : has
    API_PERMISSION ||--o{ ROLE_API_PERMISSION : has
    PROJECT ||--|| USER : owned_by
    PROJECT_MEMBER }o--|| PROJECT : belongs_to
    PROJECT_MEMBER }o--|| USER : belongs_to
    TENANT ||--o{ TENANT_PROJECT : has
    PROJECT ||--o{ TENANT_PROJECT : has

```

# API 명세
## 사용자 인증(Authentication)
|메서드|엔드포인트|설명|
|---|---|---|
|POST|/users|회원가입 (이메일 인증 포함)|
|POST|/users/email-verifications|이메일 인증 코드 확인|
|POST|/auth/tokens|로그인 (JWT 발급)|
|POST|/users/password-reset-requests|비밀번호 재설정 요청 (이메일 발송)|
|POST|/users/passwords|비밀번호 재설정|
## 역할(Role) 및 권한(Permission) 관리
|메서드|엔드포인트|설명|
|---|---|---|
|GET|/roles|역할 목록 조회|
|POST|/roles|새로운 역할 생성 (관리자)|
|POST|/roles/{role_id}/permissions|역할에 API 권한 추가|
|DELETE|/roles/{role_id}/permissions/{permission_id}|역할에서 API 권한 제거|
## 프로젝트(Project) 관리
|메서드|엔드포인트|설명|
|---|---|---|
|POST|/projects|프로젝트 생성|
|GET|/projects|프로젝트 전체 조회|
|GET|/projects/{project_id}|프로젝트 상세 조회|
|PATCH|/projects/{project_id}|프로젝트 수정 (소유자만 가능)|
|DELETE|/projects/{project_id}|프로젝트 삭제 (소유자만 가능)|
## 프로젝트 팀원 초대 및 역할 부여
|메서드|엔드포인트|설명|
|---|---|---|
|POST|/projects/{project_id}/members|프로젝트 팀원 추가|
|DELETE|/projects/{project_id}/members/{user_id}|프로젝트 팀원 제거|
