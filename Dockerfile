FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG MODE=prod
ENV MODE=${MODE}

CMD if [ "$MODE" = "dev" ]; then \
        uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload; \
    else \
        uvicorn app.main:app --host 0.0.0.0 --port 8000; \
    fi
