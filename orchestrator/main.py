from fastapi import FastAPI
import service.code_service as code_service

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("runnn")
async def runnn(format_, code1, code2, time_limit, repeat_count):
    return code_service.run(format_, code1, code2, time_limit, repeat_count)
