FROM python:3.9.19

RUN mkdir /akvalenok

WORKDIR /akvalenok

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /akvalenok/docker/*.sh

# Only for single Dockerfile
#CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
