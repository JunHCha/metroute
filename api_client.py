from typing import Literal

import aiohttp
from pydantic import BaseModel

from config import settings


class ODSayApiClient:
    def __init__(self, api_key: str, lang: Literal["ko", "eng"] = "ko") -> None:
        self.base_url = "https://api.odsay.com/v1/api"
        self.api_key = api_key
        self.lang = 0 if lang == "ko" else 1

    class SearchStationQuery(BaseModel):
        stationName: str
        CID: int = 1000
        output: str = "json"
        stationClass: int = 2
        displayCnt: int = 5

    async def get_station_code(self, params: SearchStationQuery):
        url = self.base_url + "/searchStation"
        q = params.dict(exclude_none=True) | {"apiKey": self.api_key, "lang": self.lang}
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(url, params=q) as resp:
                res = await resp.json()
                stations = res.get("result", {}).get("station", [])
                return stations[0].get("stationID") if stations else None

    class GetMetroRouteParams(BaseModel):
        SID: str  # 시작역 ID
        EID: str  # 도착역 ID
        CID: str = "1000"  # 도시코드: default=서울
        Sopt: Literal[1, 2] = 1
        output: str = "json"

    async def get_metro_route(self, params: GetMetroRouteParams):
        url = self.base_url + "/subwayPath"
        q = params.dict(exclude_none=True) | {
            "apiKey": self.api_key,
            "lang": self.lang,
        }
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(url, params=q) as resp:
                res = await resp.json()
                return res


client = ODSayApiClient(api_key=settings.ODSAY_API_KEY, lang="ko")
