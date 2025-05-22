import uvicorn
from fastapi import FastAPI

from code.code import Code

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/run_code")
async def run_code(input_name: list[str], code: Code, time_limit: int):
    return {"message": "success!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8002) #

