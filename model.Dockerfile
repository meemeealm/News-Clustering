FROM python:3.8.12-slim

WORKDIR /app  

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pipeline_bisecting.pkl pipeline_bisecting.pkl
COPY serve.py serve.py

ENV FLASK_APP=serve.py
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "serve:app"]