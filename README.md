# Thoughtful API

Small REST API with the whole CRUDL of real and fake thoughts.

Небольшое API с CRUDL для «мыслей» и токен-аутентификацией.

## Authentication

* Register API view allows to simply create a user

* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) provides an authentication for the registered user in a form of an access token available on the `/token/` route

* Login and logout views for the browsable API DRF provides are also added

## Notes

* Mind the trailing slashed :)

* Get a token using POST request with the username and password in the body

* Token is passed as a request header in a form `Authorization: Bearer eyJ0eXAiOiJKV1QiLC...` 

## To-do

- [ ] Add filter functionality

- [ ] Test

- [x] Add authentication