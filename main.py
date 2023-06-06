import datetime

import orjson
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from api_client import SeoulMetroRouteClient
from station_code import station_codes

app = FastAPI(title="metroute", openapi_url="/openapi.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.get("/logo", response_class=FileResponse)
async def logo():
    filename = "/resource/logo.png"
    return filename


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return orjson.loads(text)


class MetroRouteResponse(BaseModel):
    dept_station: str
    dest_station: str
    linenum: str


@app.get(
    "/route",
    status_code=200,
    summary="fetch subway transfer information from departure station to destination station",
)
async def get_metro_route(dept_station: str, dest_station: str):
    def _find_station_code(station_name: str) -> str | None:
        for station_code, station_name, line_num in station_codes:
            if station_name == station_name:
                return station_code
        return None

    dept_station_code = _find_station_code(dept_station)
    dest_station_code = _find_station_code(dest_station)
    if not (dept_station_code and dest_station_code):
        return []

    def _return_DAY_if_tody_is_not_weekend():
        today = datetime.datetime.today()
        if today.weekday() < 5:
            return "DAY"
        else:
            return "SAT"

    params = SeoulMetroRouteClient.QueryParams(
        serviceKey="",
        pageNo=1,
        numOfRows=1,
        dept_station_code=dept_station_code,
        dest_station_code=dest_station_code,
        week=_return_DAY_if_tody_is_not_weekend(),
    )
    client = SeoulMetroRouteClient()
    data = await client.get_dummy_metro_route(params=params)
    return data
