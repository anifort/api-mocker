# api-mocker
api-mocker is a light application that allows you to simulate API calls and responses for testing purposes.

## How to run the application
The application is build on FastAPI and therefore can run using uvicorn
> uvicorn main:app --host 0.0.0.0 --port 80 --reload

Additionally a docker file is provited.

## API Documentation

FastAPI provides OpenAPI documentation. To access it run the service and visit http://0.0.0.0:80/docs

The UI allows you to try out API requests.


## How to set an API Expectation
Before mocking an API call you need to set up an expecation using POST /mock

In the payload you need to include:
* url: The request URL you want to mock
* method: The HTTP method you will use for that URL. POST , GET, PUT, DELETE, PATCH
* response_status_code: The response status code. for example 200 or 404 or 500 etc.
* request_payload: What request payload should be in order to return the response_payload. Applicable for POST / PUT / PATCH requests
* response_payload: What request payload to return when a client calls the request URL. If none then add {}

Mock Expectations only leave in memory so on service restart you will need to reset your expectations. We recommend doing so with a script.

<br />
<br />

## Example 1: GET /user/1 

Set a mock expectation for `GET /user/1`
```curl
curl -X 'POST' \
  'http://0.0.0.0/mock' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "/user/1",
  "method": "GET",
  "request_payload": {},
  "response_status_code": 200,
  "response_payload": {
    "name": "Paul",
    "lastname": "Martin"
    }
}'
```

After using the `POST /mock` url to set your expectation, you can call your mocked URL `POST /user/create` and get the response you mocked. The mock remains in memory so you can call `POST /user/create` multiple times.

```curl
curl -X 'GET' \
  'http://0.0.0.0/user/1' \
  -H 'accept: application/json'
```

server response

```json
{
  "name": "Paul",
  "lastname": "Martin"
}
```

<br />
<br />

## Example 2: POST /user/create

Set a mock expectation for `POST /user/create`
```curl
curl -X 'POST' \
  'http://0.0.0.0/mock' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "/user/create",
  "method": "POST",
  "request_payload": {
    "name": "John",
    "lastname": "Smith"
  },
  "response_status_code": 200,
  "response_payload":  {
    "status": "created",
    "user_id": "2"
    }
}'
```

After using the `POST /mock` url to set your expectation, you can call your mocked URL `POST /user/create` and get the response you mocked. 

**Notice that the payload body must match exactly the `request_payload` as defined on the above requst body.** `request_payload` for POST/PUT/PATCH is used to create a unique signature of the request and it is used for retrieving the right expectaions. This allows to have multiple expectations to the same URL but with different request_body objects

```curl
curl -X 'POST' \
  'http://0.0.0.0/user/create' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "John",
    "lastname": "Smith"
  }'
```

server response
```json
{
  "status": "created",
  "user_id": "2"
}
```
