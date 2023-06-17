from typing import List

import orjson
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from api_client import client

app = FastAPI(title="metroute", openapi_url="/openapi.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    class Result(BaseModel):
        class DriveInfoSet(BaseModel):
            class DriveInfo(BaseModel):
                laneID: str
                laneName: str
                startName: str
                stationCount: int
                wayCode: int
                wayName: str

            driveInfo: List[DriveInfo]

        globalStartName: str
        globalEndName: str
        globalTravelTime: int
        globalDistance: int
        globalStationCount: int
        fare: int
        cashFare: int
        driveInfoSet: DriveInfoSet

        class ExChangeInfoSet(BaseModel):
            class ExChangeInfo(BaseModel):
                laneName: str
                startName: str
                exName: str
                exSID: int
                fastTrain: int
                fastDoor: int
                exWalkTime: int

            exchangeInfo: List[ExChangeInfo] | None

        exChangeInfoSet: ExChangeInfoSet | None

        class StationSet(BaseModel):
            class Stations(BaseModel):
                startID: int
                startName: str
                endSID: int
                endName: str
                travelTime: int

            stations: List[Stations]

        stationSet: StationSet

    result: Result


@app.get(
    "/route",
    status_code=200,
    response_model=MetroRouteResponse,
    description="Fetch subway transfer information from start station to end station."
    " You should enter station name only in Korean, not adding '역'"
    " at the end of the station name.",
)
async def get_metro_route(
    start_station: str,
    end_station: str,
):
    async def _find_station_code(station_name: str) -> str | None:
        params = client.SearchStationQuery(stationName=station_name)
        code = await client.get_station_code(params=params)
        return code

    dept_station_code = await _find_station_code(start_station)
    dest_station_code = await _find_station_code(end_station)
    if not (dept_station_code and dest_station_code):
        return []

    params = client.GetMetroRouteParams(SID=dept_station_code, EID=dest_station_code)
    data = await client.get_metro_route(params=params)
    return data
