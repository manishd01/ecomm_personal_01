# syntax=docker/dockerfile:1

FROM python:3.12-slim

WORKDIR /app

COPY ai-service/requirements.txt .

# CPU-only PyTorch  ---- importntm - before it was iantallling, usleess pkacges also, due to transtiive, pakcge list
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install torch --index-url https://download.pytorch.org/whl/cpu

# Other Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY ai-service/app ./app
COPY ai-service/knowledge ./knowledge

RUN mkdir -p /app/data/chroma

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]