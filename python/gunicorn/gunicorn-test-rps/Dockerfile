FROM python:3.14-alpine

RUN pip install --no-cache-dir flask gunicorn

WORKDIR /app
COPY app.py /app/app.py

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "1", "--worker-class", "gthread", "app:app"]
