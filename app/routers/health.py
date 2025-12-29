from fastapi import APIRouter
from sqlalchemy import text

from app.db.database import AsyncSessionLocal

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    db_status = "ok"

    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"

    status = "ok" if db_status == "ok" else "degraded"

    return {
        "status": status,
        "database": db_status,
    }
