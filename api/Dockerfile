FROM python:3.14

WORKDIR /app

COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ .

CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-10000}
