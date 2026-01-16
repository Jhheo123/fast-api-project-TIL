# 📁 Project Structure

```text
fast_api_project
├── alembic.ini
├── database.py
├── database_models.py
├── main.py
├── migrations
│   ├── env.py
│   └── versions
│       └── 2023_11_09_0832-382ab0927111_add_user_table.py
├── poetry.lock
├── pyproject.toml
├── user
│   ├── application
│   │   └── user_service.py
│   ├── domain
│   │   ├── repository
│   │   │   └── user_repo.py
│   │   └── user.py
│   ├── infra
│   │   ├── db_models
│   │   │   └── user.py
│   │   └── repository
│   │       └── user_repo.py
│   └── interface
│       └── controllers
│           └── user_controller.py
└── utils
    ├── __init__.py
    ├── crypto.py
    └── db_utils.py
```

---

# 🧱 Architecture Overview

본 프로젝트는 **계층형 아키텍처 (Layered Architecture)** 를 기반으로 구성되어 있습니다.

---

## 🔹 Interface Layer

**외부 요청을 처리하는 진입 계층**

* FastAPI Controller(API Endpoint) 위치
* HTTP 요청/응답 처리
* Application Layer 호출

```text
user/interface/controllers/user_controller.py
```

---

## 🔹 Application Layer

**비즈니스 유스케이스를 담당하는 계층**

* 도메인 객체 조합
* 트랜잭션 단위의 비즈니스 로직 수행
* Repository Interface 의존

```text
user/application/user_service.py
```

---

## 🔹 Domain Layer

**핵심 비즈니스 규칙을 담는 계층**

* 순수 도메인 모델 정의
* Repository 인터페이스 정의
* Framework / DB 비의존

```text
user/domain/user.py
user/domain/repository/user_repo.py
```

---

## 🔹 Infrastructure Layer

**외부 시스템(DB, ORM 등)과의 실제 구현 계층**

* ORM 모델 정의
* Repository 구현체 제공
* Domain Layer 인터페이스 구현

```text
user/infra/db_models/user.py
user/infra/repository/user_repo.py
```

---

## 🔹 Utils

**공통 유틸리티 모음**

* 암호화
* DB 헬퍼
* 범용 기능 제공

```text
utils/crypto.py
utils/db_utils.py
```

---

## 🔹 Migrations

**Alembic 기반 데이터베이스 마이그레이션 관리**

* 테이블 생성/변경 이력 관리
* 버전 기반 스키마 추적

```text
migrations/env.py
migrations/versions/*.py
```

---

# 🔄 Request Flow

```text
Client
  ↓
Controller (Interface)
  ↓
Service (Application)
  ↓
Domain Model / Repository Interface
  ↓
Repository Implementation (Infra)
  ↓
Database
```

---

# ✅ Design Principles

* 계층 간 **단방향 의존성 유지**
* Domain Layer는 **Framework 독립적**
* Repository는 **Interface / Implementation 분리**
* 테스트 및 유지보수에 유리한 구조

---