# api-mocker
api-mocker is a light application that allows you to simulate API calls and responses for testing purposes.

## How to set an API Expectation
Before mocking an API call you need to set up an expecation using POST /mock

In the payload you need to include:
* url: The request URL you want to mock
* method: The HTTP method you will use for that URL. POST , GET, PUT, DELETE, PATCH
* response_status_code: The response status code. for example 200 or 404 or 500 etc.
* request_payload: What request payload should be in order to return the response_payload. Applicable for POST / PUT / PATCH requests
* response_payload: What request payload to return when a client calls the request URL. If none then add {}

Mock Expectations only leave in memory so on service restart those expectations will be deleted.

<br />
<br />

## Example 1: GET /user/1 

Here is an example on how to set a mock expectation request `GET /user/1`
```curl
curl -X 'POST' \
  'http://0.0.0.0/mock' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "/user/1",
  "method": "GET",
  "response_status_code": 200,
  "request_payload": {},
  "response_payload": {
    "name": "Paul",
    "lastname": "Martin"
    }
}'
```

After using the `POST /mock` url to set your expectation for `POST /user/create` , you can now `POST /user/create` and get the response you mocked.

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

Here is an example on how to set a mock expectation request `POST /user/create`
```curl
curl -X 'POST' \
  'http://0.0.0.0/mock' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "/user/create",
  "method": "POST",,
  "request_payload": {
    "name": "John",
    "lastname": "Smith"
  },
  "response_status_code": 200
  "response_payload":  {
    "status": "created",
    "user_id": "2"
    }
}'
```

After using the `POST /mock` url to set your expectation for `POST /user/create` , you can now `POST /user/create` and get the response you mocked.

```curl
curl -X 'POST' \
  'http://0.0.0.0/user/create' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Paul",
  "lastname": "Martin"
}'
```

server response

```json
{
  "status": "created",
  "user_id": "2"
}
```
