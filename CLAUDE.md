# Project Guidelines

## 언어

- 코드 주석: 영어
- 커밋 메시지: 한국어
- 대화 및 설명: 한국어

## 프로젝트 구조

```
app/
├── main.py          # FastAPI 앱 진입점
├── config.py        # pydantic-settings 설정
├── routers/         # API 엔드포인트
├── services/        # 비즈니스 로직
├── models/          # SQLAlchemy 모델
└── db/              # 데이터베이스 설정
```

## 코드 스타일

- Python 3.13+ 문법 사용
- Type hints 필수
- async/await 패턴 사용 (SQLAlchemy, HTTP 클라이언트 등)
- 함수/클래스 docstring은 필요한 경우에만 간결하게

## API 설계

- RESTful 규칙 준수
- 응답은 JSON 형식
- 에러 응답: `{"detail": "에러 메시지"}`
- 새 엔드포인트는 `app/routers/`에 별도 파일로 생성

## 데이터베이스

- SQLAlchemy 2.0 async 패턴 사용
- 모델 변경 시 Alembic 마이그레이션 생성 필수
- 마이그레이션 메시지도 한국어로 작성

## 환경 설정

- 모든 설정은 `.env`와 `app/config.py`로 관리
- 새 환경변수 추가 시 `.env.example`도 함께 업데이트
- 민감한 정보(시크릿, 비밀번호)는 절대 코드에 하드코딩 금지

## Git Commit Convention

커밋 메시지는 **Conventional Commits** 형식을 따르며, **한국어**로 작성한다.

### 형식

```
<type>(<scope>): <설명>

[본문 - 선택사항]
```

### Type

- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 변경
- `style`: 코드 포맷팅 (동작 변경 없음)
- `refactor`: 리팩토링 (기능 변경 없음)
- `test`: 테스트 추가/수정
- `chore`: 빌드, 설정, 의존성 등

### Scope (선택)

변경된 모듈/영역: `api`, `db`, `deploy`, `docker`, `config` 등

### 예시

```
feat(api): 사용자 인증 엔드포인트 추가
fix(db): 커넥션 풀 타임아웃 문제 해결
chore(docker): Caddy 리버스 프록시 설정 추가
```

### 규칙

- 설명은 50자 이내로 간결하게
- 명령형으로 작성 ("추가", "수정", "변경")
- 마침표 생략

## 테스트

- 새 기능 추가 시 테스트 작성 권장
- 테스트 파일: `tests/` 디렉토리
- pytest 사용

## Docker

- 프로덕션: `docker compose up -d`
- 개발: `docker compose --profile dev up api-dev`
- 이미지 재빌드: `docker compose build --no-cache`
