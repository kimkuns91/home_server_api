# Home Server API

홈서버용 FastAPI 백엔드 서버

## 기술 스택

- **Python 3.13** / FastAPI / Uvicorn
- **PostgreSQL** + SQLAlchemy 2.0 (async) + Alembic
- **Docker** + Docker Compose
- **nginx** (리버스 프록시, 호스트에서 관리)

## 프로젝트 구조

```
├── app/
│   ├── main.py              # FastAPI 앱 진입점
│   ├── config.py            # 환경 설정
│   ├── routers/             # API 엔드포인트
│   ├── schemas/             # Pydantic 요청/응답 스키마
│   ├── services/            # 비즈니스 로직
│   ├── models/              # SQLAlchemy 모델
│   ├── repositories/        # DB 쿼리 로직
│   ├── db/                  # 데이터베이스 설정
│   └── core/                # 공통 유틸, 예외, 의존성
├── alembic/                 # DB 마이그레이션
├── Dockerfile
├── docker-compose.yml
└── deploy.sh                # 자동 배포 스크립트
```

## 설치

### 1. 저장소 클론

```bash
git clone https://github.com/kimkuns91/home_server_api.git
cd home_server_api
```

### 2. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일 수정
```

### 3. PostgreSQL 설정

```sql
CREATE USER home_api_user WITH PASSWORD 'your-password';
CREATE DATABASE home_server_api OWNER home_api_user;
```

## 실행

### 로컬 개발 (Docker 없이)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker 개발 모드 (hot reload)

```bash
docker compose --profile dev up api-dev
```

### Docker 프로덕션

```bash
docker compose up -d
```

### 컨테이너 재빌드

```bash
docker compose build --no-cache
docker compose up -d
```

## 환경 변수

| 변수 | 설명 | 예시 |
|------|------|------|
| `APP_NAME` | 앱 이름 | Home Server API |
| `DEBUG` | 디버그 모드 | false |
| `DATABASE_URL` | PostgreSQL 연결 | postgresql+asyncpg://user:pass@host:5432/db |
| `GITHUB_WEBHOOK_SECRET` | 웹훅 시크릿 | your-secret |

## 데이터베이스 마이그레이션

```bash
# 마이그레이션 생성
alembic revision --autogenerate -m "설명"

# 마이그레이션 적용
alembic upgrade head

# 롤백
alembic downgrade -1
```

## API 문서

서버 실행 후:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 배포

### 자동 배포 (GitHub Webhook)

1. GitHub repo → Settings → Webhooks → Add webhook
2. **Payload URL**: `https://api.whitemouse.dev/webhook/github`
3. **Content type**: `application/json`
4. **Secret**: `.env`의 `GITHUB_WEBHOOK_SECRET`과 동일
5. **Events**: `push` 선택

> main 브랜치에 push할 때만 자동 배포됩니다.

### 수동 배포

```bash
./deploy.sh
```

### nginx 설정 예시

```nginx
server {
    listen 80;
    server_name api.whitemouse.dev;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 개발 가이드

프로젝트 규칙은 [CLAUDE.md](CLAUDE.md) 참고
