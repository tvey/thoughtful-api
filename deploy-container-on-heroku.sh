heroku stack:set container -a the-thoughtful-api

docker build -t tho -f Dockerfile-heroku . --no-cache

docker tag tho registry.heroku.com/the-thoughtful-api/web

heroku container:login

docker push registry.heroku.com/the-thoughtful-api/web

heroku container:release web -a the-thoughtful-api

heroku run python manage.py migrate -a the-thoughtful-api