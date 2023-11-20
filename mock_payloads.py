from pydantic import BaseModel, Field

class MockRequestBuilder(BaseModel):
    
    url: str | None = Field(
        default=None, 
        title="The request URL you want to mock", 
        example= "/user/1"
    )

    method: str | None = Field(
        default=None, 
        title="The HTTP method you will use for that URL. POST , GET, PUT, DELETE, PATCH", 
        example= "GET"
    )

    response_status_code: int | None  = Field(
        default=200, 
        title="The response status code. for example 200 or 404 or 500 etc..", 
        example= "200"
    )

    response_payload: dict | None  = Field(
        default={}, 
        title="What request payload to return when a client calls the request URL", 
        example='{"name": "Paul", "lastname":"Martin"}'
    )