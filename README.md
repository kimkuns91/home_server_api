# Home Server API

홈서버용 FastAPI 백엔드 서버

## 기술 스택

- **Python 3.13** / FastAPI / Uvicorn
- **PostgreSQL** + SQLAlchemy 2.0 (async) + Alembic
- **Docker** + Docker Compose
- **Caddy** (리버스 프록시)

## 프로젝트 구조

```
├── app/
│   ├── main.py           # FastAPI 앱
│   ├── config.py         # 환경 설정
│   ├── routers/          # API 엔드포인트
│   ├── services/         # 비즈니스 로직
│   ├── models/           # SQLAlchemy 모델
│   └── db/               # 데이터베이스 설정
├── alembic/              # DB 마이그레이션
├── Dockerfile
├── docker-compose.yml
├── Caddyfile
└── deploy.sh             # 자동 배포 스크립트
```

## 실행 방법

### 로컬 개발

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker (개발 모드)

```bash
docker compose --profile dev up api-dev
```

### Docker (프로덕션)

```bash
docker compose up -d
```

## 환경 설정

`.env.example`을 `.env`로 복사 후 수정:

```bash
cp .env.example .env
```

| 변수 | 설명 |
|------|------|
| `APP_NAME` | 앱 이름 |
| `DEBUG` | 디버그 모드 |
| `DATABASE_URL` | PostgreSQL 연결 문자열 |
| `GITHUB_WEBHOOK_SECRET` | GitHub 웹훅 시크릿 |

## 데이터베이스

### PostgreSQL 설정

```sql
CREATE USER home_api_user WITH PASSWORD 'your-password';
CREATE DATABASE home_server_api OWNER home_api_user;
```

### 마이그레이션

```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "설명"

# 마이그레이션 적용
alembic upgrade head
```

## API 문서

서버 실행 후:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 배포

GitHub push 시 웹훅을 통해 자동 배포:

1. GitHub repo → Settings → Webhooks → Add webhook
2. Payload URL: `https://api.whitemouse.dev/webhook/github`
3. Secret: `.env`의 `GITHUB_WEBHOOK_SECRET`과 동일하게 설정
4. Events: `push`

수동 배포:

```bash
./deploy.sh
```
