from pydantic import BaseModel, Field
from typing import Optional

class MockRequestBuilder(BaseModel):

    url: str = Field(
        description="The request URL you want to mock", 
        example= "/user/1"
    )

    method: str = Field(
        description="The HTTP method you will use for that URL. POST , GET, PUT, DELETE, PATCH", 
        example= "GET"
    )

    response_status_code: int | None  = Field(
        default=200, 
        description="The response status code. for example 200 or 404 or 500 etc..", 
        example= "200"
    )
    
    request_payload: Optional[dict] | None  = Field(
        default=None, 
        description="What request payload is needed for returning the response below. Used for POST, PUT and PATCH requests", 
        example='{}'
    )

    response_payload: dict  = Field(
        description="What response payload to return when a client calls the request URL", 
        example='{"name": "Paul", "lastname":"Martin"}'
    )

class Payload(BaseModel):

    def dummy():
        return
    
    