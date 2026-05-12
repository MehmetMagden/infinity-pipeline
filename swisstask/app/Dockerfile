FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq5 \
    && rm -rf /var/lib/apt/lists/*


COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY app.py .

RUN useradd -m swisstaskuser
USER swisstaskuser

EXPOSE 5000

CMD ["python", "app.py"]