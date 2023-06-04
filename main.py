from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="metroute", openapi_url="/openapi.json")


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.get("/logo.png", response_class=FileResponse)
async def logo():
    filename = "logo.png"
    return filename
