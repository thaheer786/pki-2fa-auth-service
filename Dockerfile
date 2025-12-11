# ---------- Builder ----------
FROM python:3.11-slim AS builder
WORKDIR /build

# Install build essentials for cryptography
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies into virtual environment
COPY app/requirements.txt ./requirements.txt

RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt


# ---------- Runtime ----------
FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app

# Install cron + tzdata
RUN apt-get update && apt-get install -y --no-install-recommends cron tzdata ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy python virtual environment
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY app /app
COPY scripts /app/scripts
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Copy RSA keys
COPY student_private.pem student_public.pem instructor_public.pem /app/

# Create runtime directories
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Setup cron job
RUN chmod 0644 /etc/cron.d/2fa-cron && crontab /etc/cron.d/2fa-cron
RUN chmod +x /app/scripts/log_2fa_cron.py

EXPOSE 8080

CMD service cron start && uvicorn app.main:app --host 0.0.0.0 --port 8080
