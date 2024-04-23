FROM python:3.12-alpine AS builder

WORKDIR /app

COPY requirements.txt ./

RUN apk add --no-cache py3-pip
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12

WORKDIR /app

COPY . .

# Install Alembic in the final image
RUN pip install alembic

# Specify the location of alembic.ini
ENV ALEMBIC_CONFIG=/app/alembic.ini

# Run Alembic migration
RUN alembic upgrade head

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
