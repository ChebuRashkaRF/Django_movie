FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/django_movie

RUN pip install --upgrade pip
COPY ./reqs.txt /app
RUN pip install -r /app/reqs.txt

COPY . .

EXPOSE 8000
