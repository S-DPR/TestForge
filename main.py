from fastapi import FastAPI

from request.config_structs import TestcaseConfig
from request.executor import process

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/create/testcase")
async def create_testcase(testcase: TestcaseConfig):
    return process(testcase)
