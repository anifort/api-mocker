from fastapi import FastAPI, Request, status, Body
from mock_payloads import MockRequestBuilder
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
import json, logging
import hashlib 
from typing import Annotated
app = FastAPI(title="Chat API", version="1.0.0")

app.memory = { 
        "GET": {}, 
        "POST": {},
        "PUT": {}, 
        "PATCH": {},
        "DELETE": {}
    }

def initialise():
    
    return
   

@app.on_event("startup")
async def startup_event():
    initialise()

def get_sha(content: dict) -> str:
    return hashlib.sha256(json.dumps(content).encode('utf-8')).hexdigest()

def get_req_payload_sha(request) -> str:
    if request is None:
        return "none"
   
    request_payload = request.get('request_payload', {})
    if not request_payload:
        return "none"
    else:
        return get_sha(request_payload)


@app.post(
    path = "/mock", 
    description="Chat endpoint that uses Enterprise Search as information retrieval source", 
    status_code=200)
async def mock(request: MockRequestBuilder):
    if request.method.upper() not in ["POST","GET","PUT","DELETE","PATCH"]:
        raise Exception("Invalid Mock HTTP Method")
  
    payload_sha = get_req_payload_sha(request.__dict__) 
    app.memory = {
        request.method.upper(): { 
            request.url: {
                payload_sha: {
                    "status_code": request.response_status_code,
                    "content": request.response_payload 
                }
            }
        }
    }

    return {"message": f"mock expectations for {request.method.upper()} {request.url} set successfully", "request_payload_sha": payload_sha}

def process_request(full_path: str, request: dict, method: str):
    path = f"/{full_path}"
    if path not in app.memory[method]:  
        return JSONResponse(status_code=status.HTTP_417_EXPECTATION_FAILED, content={"message": f"Expectation for {method} {path} not configured"})

    payload_sha = get_sha(request)
    payload = app.memory[method][path][payload_sha]
    return JSONResponse(status_code=payload.get('status_code'), content=payload.get('content')) 

@app.post("/{full_path:path}")
@app.put("/{full_path:path}")
@app.patch("/{full_path:path}")
async def catch_all(full_path: str, body: Annotated[dict, Body()], request: Request):
    return process_request(full_path, body, request.method)


@app.get("/{full_path:path}")
@app.delete("/{full_path:path}")
async def catch_all(full_path: str, request: Request): 
    path = f"/{full_path}"
    if path not in app.memory[request.method.upper()]:  
        return JSONResponse(status_code=status.HTTP_417_EXPECTATION_FAILED, content={"message": f"Expectation for {request.method} {path} not configured"})
    
    payload_sha = get_req_payload_sha(request)
    payload = app.memory[request.method.upper()][path][payload_sha]

    return JSONResponse(status_code=payload.get('status_code'), content=payload.get('content'))