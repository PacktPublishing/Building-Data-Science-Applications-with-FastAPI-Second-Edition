FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

ENV APP_MODULE project.app:app

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

COPY ./ /app
