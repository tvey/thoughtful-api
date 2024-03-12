# Thoughtful API

Small REST API with the whole CRUDL of real and fake thoughts.

Небольшое API с CRUDL для «мыслей» и токен-аутентификацией.

## Endpoints

The API endpoints include thoughts, tags, and authors, as well as some routes for users.

The list of created routes is available on the base url of the project.

## Authentication

* `register` API view allows creating a user from POSTed.

```json
{
  "username": "user123",
  "password": "eto-secret",
  "password2": "eto-secret"
}
```

* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) provides authentication for the registered user in a form of an access token available on the `/token/` route.

* `login` and `logout` views and routes which DRF provides for the browsable API are also added.

## Notes

* All visible REST deviations (base path, customized pagination etc.) are for sheer exploration and for making things look the way it was initially desired.

* Get a token using a POST request with the username and password in the body.

* Token is passed as a request header (Bearer token) in the form `Authorization: Bearer eyJ0eXAiOiJKV1QiLC...`
