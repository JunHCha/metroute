from fastapi import FastAPI

app = FastAPI(title="metroute", openapi_url="/openapi.json")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping")
async def ping():
    return {"message": "pong"}
