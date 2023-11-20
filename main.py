from fastapi import FastAPI, Request, status
from mock_payloads import MockRequestBuilder
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
import json, logging

app = FastAPI(title="Chat API", version="1.0.0")

app.memory = { }

def initialise():
    app.memory = { 
        "GET": {}, 
        "POST": {},
        "PUT": {}, 
        "PATCH": {},
        "DELETE": {}
    }
    return
   

@app.on_event("startup")
async def startup_event():
    initialise()



@app.post(
    path = "/mock", 
    description="Chat endpoint that uses Enterprise Search as information retrieval source", 
    status_code=200)
async def mock(payload: MockRequestBuilder):
    if payload.method.upper() not in ["POST","GET","PUT","DELETE","PATCH"]:
        raise Exception("Invalid Mock HTTP Method")

    app.memory = {
        payload.method.upper(): { 
            payload.url: {
                "status_code": payload.response_status_code,
                "content": payload.response_payload 
            }
        }
    }

    return {"message": f"mock expectations for {payload.method.upper()} {payload.url} set successfully"}



@app.get("/{full_path:path}")
@app.post("/{full_path:path}")
@app.put("/{full_path:path}")
@app.patch("/{full_path:path}")
@app.delete("/{full_path:path}")
async def catch_all(request: Request, full_path: str): 
    print(app.memory)
    path = f"/{full_path}"
    if path not in app.memory[request.method.upper()]:  
        return JSONResponse(status_code=status.HTTP_417_EXPECTATION_FAILED, content={"message": f"Expectation for {request.method} {path} not configured"})
    
    payload = app.memory[request.method.upper()][path]
    return JSONResponse(status_code=payload.get('status_code'), content=payload.get('content'))

