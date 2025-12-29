#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/deploy.log"
BACKUP_TAG="backup-$(date +%Y%m%d-%H%M%S)"

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

rollback() {
    log "ERROR: Deployment failed. Rolling back..."

    if git rev-parse "$BACKUP_TAG" >/dev/null 2>&1; then
        git checkout "$BACKUP_TAG" -- .
        log "Rolled back to $BACKUP_TAG"
    fi

    if docker compose ps --quiet 2>/dev/null | grep -q .; then
        log "Restarting previous containers..."
        docker compose up -d --build api
    fi

    log "Rollback completed"
    exit 1
}

trap rollback ERR

log "========== Deployment started =========="

# Save current state
CURRENT_COMMIT=$(git rev-parse HEAD)
log "Current commit: $CURRENT_COMMIT"
git tag -f "$BACKUP_TAG" "$CURRENT_COMMIT"

# Pull latest changes
log "Pulling latest changes..."
git fetch origin
git pull origin "$(git rev-parse --abbrev-ref HEAD)"

NEW_COMMIT=$(git rev-parse HEAD)
log "New commit: $NEW_COMMIT"

if [ "$CURRENT_COMMIT" = "$NEW_COMMIT" ]; then
    log "No changes detected. Skipping rebuild."
    git tag -d "$BACKUP_TAG" 2>/dev/null || true
    exit 0
fi

# Rebuild and restart
log "Stopping containers..."
docker compose down

log "Rebuilding containers..."
docker compose build --no-cache api

log "Starting containers..."
docker compose up -d api

# Health check
log "Waiting for health check..."
sleep 5

HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "000")

if [ "$HEALTH_STATUS" != "200" ]; then
    log "Health check failed (status: $HEALTH_STATUS)"
    rollback
fi

log "Health check passed"

# Cleanup backup tag
git tag -d "$BACKUP_TAG" 2>/dev/null || true

log "========== Deployment completed successfully =========="
