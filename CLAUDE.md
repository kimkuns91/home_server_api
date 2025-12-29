# Project Guidelines

## 언어

- 코드 주석: 영어
- 커밋 메시지: 한국어
- 대화 및 설명: 한국어

## 프로젝트 구조

```
app/
├── main.py              # FastAPI 앱 진입점
├── config.py            # pydantic-settings 환경 설정
├── routers/             # API 엔드포인트 (얇게 유지)
├── schemas/             # Pydantic 요청/응답 스키마
├── services/            # 비즈니스 로직
├── models/              # SQLAlchemy ORM 모델
├── repositories/        # DB 쿼리 로직 (CRUD 추상화)
├── db/                  # DB 연결 및 세션 관리
└── core/                # 공통 유틸리티, 예외, 의존성
```

### 레이어별 책임

| 레이어 | 책임 | 의존 가능 |
|--------|------|-----------|
| `routers/` | HTTP 요청/응답 처리, 입력 검증 | schemas, services |
| `schemas/` | 데이터 직렬화/역직렬화, 검증 | - |
| `services/` | 비즈니스 로직, 트랜잭션 관리 | repositories, models |
| `repositories/` | DB CRUD 연산 추상화 | models, db |
| `models/` | 테이블 정의, 관계 설정 | - |
| `core/` | 공통 기능 (예외, 의존성, 유틸) | - |

### 레이어 규칙

- **Router는 얇게**: 비즈니스 로직 금지, Service 호출만
- **Service에 로직 집중**: 트랜잭션, 검증, 외부 API 호출
- **Repository로 DB 분리**: 직접 쿼리는 Repository에서만
- **순환 참조 금지**: 상위 레이어만 하위 레이어 import

## 네이밍 컨벤션

### 파일명

- 모두 **snake_case**: `user_service.py`, `item_schema.py`
- 라우터: `{resource}.py` (예: `users.py`, `items.py`)
- 스키마: `{resource}.py` (예: `user.py`, `item.py`)
- 서비스: `{resource}_service.py`
- 리포지토리: `{resource}_repository.py`

### 클래스명

- Pydantic 스키마: `{Resource}{Action}` (예: `UserCreate`, `UserResponse`, `ItemUpdate`)
- SQLAlchemy 모델: `{Resource}` (예: `User`, `Item`)
- 서비스: `{Resource}Service` (예: `UserService`)
- 리포지토리: `{Resource}Repository` (예: `UserRepository`)

### 함수명

- 동사로 시작: `get_`, `create_`, `update_`, `delete_`, `find_`, `check_`
- async 함수도 동일 규칙

## 코드 스타일

### 필수

- Python 3.13+ 문법
- Type hints 100% 적용
- async/await 일관 사용
- f-string 사용 (`.format()`, `%` 금지)

### 금지

- `Any` 타입 남용 (불가피한 경우만)
- `*args`, `**kwargs` 남용
- 중첩 함수 3단계 이상
- 하나의 함수 50줄 초과
- 전역 변수 (상수 제외)

### 권장

- Early return 패턴
- Guard clause로 예외 먼저 처리
- 컴프리헨션 적절히 사용 (복잡하면 for문)
- dataclass, Enum 적극 활용

## API 설계

### URL 규칙

- 복수형 리소스: `/users`, `/items`
- 계층 관계: `/users/{user_id}/orders`
- 행위는 HTTP 메서드로: GET, POST, PUT, PATCH, DELETE
- 검색/필터: 쿼리 파라미터 사용

### 응답 형식

```python
# 성공
{"data": {...}, "message": "success"}

# 목록
{"data": [...], "total": 100, "page": 1, "size": 20}

# 에러
{"detail": "에러 메시지", "code": "ERROR_CODE"}
```

### HTTP 상태 코드

- `200`: 성공 (GET, PUT, PATCH)
- `201`: 생성됨 (POST)
- `204`: 내용 없음 (DELETE)
- `400`: 잘못된 요청
- `401`: 인증 필요
- `403`: 권한 없음
- `404`: 리소스 없음
- `422`: 유효성 검증 실패
- `500`: 서버 오류

## 예외 처리

### 커스텀 예외 사용

```python
# core/exceptions.py에 정의
class NotFoundError(Exception): ...
class ValidationError(Exception): ...
class AuthenticationError(Exception): ...
```

### 예외 처리 규칙

- Service 레이어에서 비즈니스 예외 발생
- Router에서 HTTP 예외로 변환
- 예외 메시지는 사용자 친화적으로
- 스택 트레이스는 로그에만 (프로덕션)

## 데이터베이스

### SQLAlchemy 규칙

- 2.0 스타일 async 쿼리 사용
- `select()` 문 사용 (`session.query()` 금지)
- Lazy loading 피하기 (`selectinload`, `joinedload` 명시)
- N+1 쿼리 주의

### 모델 규칙

```python
class User(Base):
    __tablename__ = "users"

    # PK
    id: Mapped[int] = mapped_column(primary_key=True)

    # 필수 필드
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    # 선택 필드
    name: Mapped[str | None] = mapped_column(String(100))

    # 타임스탬프 (모든 모델에 포함)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
```

### 마이그레이션

- 모델 변경 시 반드시 Alembic 마이그레이션 생성
- 마이그레이션 메시지 한국어
- 프로덕션 배포 전 마이그레이션 테스트 필수

## 환경 설정

- 모든 설정은 `.env` + `config.py`로 관리
- 새 환경변수 추가 시 `.env.example` 동시 업데이트
- 시크릿 하드코딩 절대 금지
- 환경별 설정 분기는 `DEBUG` 플래그 활용

## 보안

- SQL Injection: ORM 파라미터 바인딩 사용
- XSS: 응답 자동 이스케이프 확인
- CORS: 명시적 origin 설정
- 인증: JWT 또는 세션 기반
- 비밀번호: bcrypt 해싱 (평문 저장 금지)
- 민감 정보: 로그에 출력 금지

## 로깅

```python
import logging
logger = logging.getLogger(__name__)

# 레벨별 용도
logger.debug("개발 디버깅용")
logger.info("정상 동작 기록")
logger.warning("주의 필요한 상황")
logger.error("에러 발생", exc_info=True)
```

## Git Commit Convention

커밋 메시지는 **Conventional Commits** 형식, **한국어**로 작성.

### 형식

```
<type>(<scope>): <설명>

[본문 - 선택사항]
```

### Type

| Type | 설명 |
|------|------|
| `feat` | 새로운 기능 |
| `fix` | 버그 수정 |
| `docs` | 문서 변경 |
| `style` | 포맷팅 (동작 변경 없음) |
| `refactor` | 리팩토링 |
| `test` | 테스트 |
| `chore` | 빌드, 설정 |

### Scope

`api`, `db`, `auth`, `deploy`, `docker`, `config` 등

### 예시

```
feat(api): 사용자 회원가입 엔드포인트 추가
fix(db): 커넥션 풀 타임아웃 문제 해결
refactor(service): UserService 로직 분리
```

## 테스트

- 위치: `tests/` 디렉토리
- 프레임워크: pytest + pytest-asyncio
- 네이밍: `test_{module}.py`, `test_{기능}()`
- 커버리지 목표: 80% 이상 (핵심 로직)

## Docker

```bash
# 프로덕션
docker compose up -d

# 개발 (hot reload)
docker compose --profile dev up api-dev

# 재빌드
docker compose build --no-cache
```
