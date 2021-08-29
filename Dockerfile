FROM python:3.9.6-alpine

ENV PYTHONUNBUFFERED=true
ENV PYTHONDONTWRITEBYTECODE=true

WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]