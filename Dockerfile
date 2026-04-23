FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Only install libpq-dev if you use the standard psycopg2. 
# If you stick with psycopg2-binary, you can actually remove build-essential.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \ 
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy only the app folder to keep the image clean
COPY ./app ./app
# Copy the migrations and config files
COPY ./alembic.ini .
COPY .env.docker . 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]