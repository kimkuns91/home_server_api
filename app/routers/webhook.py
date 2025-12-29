import hmac
import hashlib
import logging
import subprocess
from pathlib import Path

from fastapi import APIRouter, Request, HTTPException, BackgroundTasks, Depends

from app.config import Settings, get_settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhook"])

DEPLOY_SCRIPT = Path(__file__).parent.parent.parent / "deploy.sh"
DEPLOY_BRANCH = "refs/heads/main"


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    if not signature.startswith("sha256="):
        return False

    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(f"sha256={expected}", signature)


def run_deploy(branch: str) -> None:
    logger.info(f"Deployment started for branch: {branch}")

    try:
        result = subprocess.run(
            ["bash", str(DEPLOY_SCRIPT)],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            logger.info(f"Deployment completed successfully for branch: {branch}")
        else:
            logger.error(
                f"Deployment failed for branch: {branch}, "
                f"exit code: {result.returncode}, "
                f"stderr: {result.stderr}"
            )
    except Exception as e:
        logger.error(f"Deployment error for branch: {branch}, exception: {e}")


@router.post("/github")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    settings: Settings = Depends(get_settings),
):
    if not settings.github_webhook_secret:
        raise HTTPException(status_code=500, detail="Webhook secret not configured")

    signature = request.headers.get("X-Hub-Signature-256", "")
    payload = await request.body()

    if not verify_signature(payload, signature, settings.github_webhook_secret):
        raise HTTPException(status_code=401, detail="Invalid signature")

    event = request.headers.get("X-GitHub-Event", "")

    if event == "ping":
        logger.info("Received ping event from GitHub")
        return {"message": "pong"}

    if event == "push":
        data = await request.json()
        ref = data.get("ref", "")
        branch = ref.replace("refs/heads/", "") if ref.startswith("refs/heads/") else ref

        logger.info(f"Push event received from branch: {branch}")

        if ref != DEPLOY_BRANCH:
            logger.info(f"Skipping deployment - branch '{branch}' is not main")
            return {"message": "ok"}

        background_tasks.add_task(run_deploy, branch)
        return {"message": "Deployment queued", "branch": branch}

    logger.info(f"Ignoring event: {event}")
    return {"message": "ok"}
