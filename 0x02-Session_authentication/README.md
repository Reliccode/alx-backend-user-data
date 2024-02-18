# 📖 0x01. Basic authentication.

- 💻 REST API Authentication Mechanisms
- 💻 HTTP header Authorization
- 💻 Flask, and
- 💻 Base64 concepts.

## Installation
Download and start your project from this [archive.zip](https://github.com/faustine-van/alx-backend-user-data/blob/master/0x01-Basic_authentication/ec2f874b061bd3a2915949f081f4f5f055104f20.zip)

`unzip ec2f874b061bd3a2915949f081f4f5f055104f20.zip`

In this archive, you will find a simple API with one model:
User. Storage of these users is done via a serialization/deserialization in files.


## Simple API

Simple HTTP API for playing with `User` model.


### Files

#### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

#### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints


- `auth/auth.py`: contains class to manage the API authentication.
- `views/basic_auth.py`:  sub class to manage the API authentication.

### Setup

```
$ pip3 install -r requirements.txt
```


## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
API_HOST=0.0.0.0 API_PORT=5000 ./main_4.py
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)

- `GET /users/me`: return current user based on authenticaticatin



### Reference 
1. [REST API Authentication Mechanisms](https://www.youtube.com/watch?v=501dpx2IjGY)
2. [HTTP header Authorization](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization)
3. [Base64 concepts.](https://docs.python.org/3/library/base64.html?utm_campaign=ALX+-+2023+-+SE+Cohort+13&utm_medium=email&_hsmi=82680881&_hsenc=p2ANqtz-9IE9hfhkVUI85UMieLP96s3-xDU4NyVRgHzNy1fb5rjQFiIWIF6aNlbEfke9o2kRvkJgaEkmK0i7aTy1a3-B7v3Zvgxny9b0aKWX80iYE2QyBgSQY&utm_content=82680881&utm_source=hs_email#module-base64)
4. [Custom Error Pages](https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/)
5. [HTTP Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cookie)
5. [Flask Cookie](https://flask.palletsprojects.com/en/1.1.x/quickstart/#cookies)
