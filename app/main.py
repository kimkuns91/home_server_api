from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import health, webhook

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_real_ip(request: Request, call_next):
    # X-Real-IP from nginx/proxy
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        request.state.client_ip = real_ip
    else:
        request.state.client_ip = request.client.host if request.client else None

    return await call_next(request)


app.include_router(health.router)
app.include_router(webhook.router)


@app.get("/")
async def root():
    return {"message": "Home Server API", "docs": "/docs"}
