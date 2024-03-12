FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install --no-cache-dir pipenv
COPY Pipfile* ./
RUN pipenv requirements > requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . ./

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
