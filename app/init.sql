-- ✅ 테넌트(조직) 테이블 생성
CREATE TABLE IF NOT EXISTS tenants (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL
);

-- ✅ 역할(Role) 테이블 생성
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL
);

-- ✅ API 권한 테이블 생성
CREATE TABLE IF NOT EXISTS api_permissions (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    endpoint VARCHAR NOT NULL,
    method VARCHAR NOT NULL
);

-- ✅ 역할-API 권한 연결 테이블 (다대다 관계)
CREATE TABLE IF NOT EXISTS role_api_permission (
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    api_permission_id INTEGER REFERENCES api_permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, api_permission_id)
);

-- ✅ 프로젝트 테이블 생성
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    owner_id INTEGER REFERENCES roles(id) ON DELETE CASCADE
);

-- ✅ 프로젝트 팀원 테이블 (다대다 관계)
CREATE TABLE IF NOT EXISTS project_members (
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (project_id, user_id)
);

-- ✅ 기본 테넌트 추가
INSERT INTO tenants (id, name) VALUES (0, 'Default Tenant') ON CONFLICT (id) DO NOTHING;

-- ✅ 기본 역할(Role) 삽입
INSERT INTO roles (id, name) VALUES
(1, 'Admin'),
(2, 'Project Owner'),
(3, 'Editor'),
(4, 'Viewer')
ON CONFLICT (id) DO NOTHING;

-- ✅ API 권한(Action) 삽입
INSERT INTO api_permissions (id, name, endpoint, method) VALUES
(1, 'Create Project', '/projects', 'POST'),
(2, 'Invite Members & Assign Roles', '/projects/{project_id}/members', 'POST'),
(3, 'Edit Project', '/projects/{project_id}', 'PATCH'),
(4, 'View Project', '/projects/{project_id}', 'GET'),
(5, 'Delete Project', '/projects/{project_id}', 'DELETE'),
(6, 'Delete User Account', '/users/{user_id}', 'DELETE')
ON CONFLICT (id) DO NOTHING;

-- ✅ 역할별 API 권한 매핑
-- Admin
INSERT INTO role_api_permission (role_id, api_permission_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)
ON CONFLICT DO NOTHING;

-- Project Owner
INSERT INTO role_api_permission (role_id, api_permission_id) VALUES
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5)
ON CONFLICT DO NOTHING;

-- Editor
INSERT INTO role_api_permission (role_id, api_permission_id) VALUES
(3, 3), (3, 4)
ON CONFLICT DO NOTHING;

-- Viewer (기본 권한)
INSERT INTO role_api_permission (role_id, api_permission_id) VALUES
(4, 4)
ON CONFLICT DO NOTHING;
