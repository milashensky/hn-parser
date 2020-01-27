FROM python:3.7
ENV PYTHONUNBUFFERED 1

COPY . ./app
WORKDIR /app

RUN pip install -r requirements/base.txt
