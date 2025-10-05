# ---------- Build stage ----------
FROM python:3.10-alpine3.19 AS builder

# RUN apk add --no-cache build-base

WORKDIR /app
COPY requirements.txt .

# Create venv and install dependencies
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ---------- Final stage ----------
FROM python:3.10-alpine3.19

# Copy venv from builder
COPY --from=builder /opt/venv /opt/venv

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Nonroot user and curl for healthcheck
RUN adduser -D nonroot && apk add --no-cache curl
USER nonroot
WORKDIR /home/app


COPY --chown=nonroot:nonroot . .

# Healthcheck and port exposure
EXPOSE 5000
HEALTHCHECK CMD curl -f http://localhost:5000/ || exit 1

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
