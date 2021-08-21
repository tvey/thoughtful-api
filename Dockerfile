FROM python:3.9-alpine

ENV PYTHONUNBUFFERED=true
ENV PYTHONDONTWRITEBYTECODE=true

WORKDIR /app

RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --skip-lock --system --dev

COPY . .