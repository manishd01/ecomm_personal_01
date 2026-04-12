FROM python:3.9-slim

WORKDIR /app

# Install netcat for wait script
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Step 1: copy only requirements
COPY notification-service/requirements.txt .

# Step 2: install dependencies (cached)
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Step 3: copy rest of code
COPY notification-service /app

# Copy entrypoint script
COPY notification-service/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PYTHONPATH=/app

CMD ["sh", "/app/entrypoint.sh"]