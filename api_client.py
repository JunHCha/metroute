from typing import Literal

import aiohttp
import orjson
from pydantic import BaseModel


class SeoulMetroRouteClient:
    base_url = "http://apis.data.go.kr/B553766/smt-path/path"

    class QueryParams(BaseModel):
        serviceKey: str
        pageNo: int
        numOfRows: int
        dept_station_code: str
        dest_station_code: str
        week: Literal["DAY", "SAT", "SUN"]
        search_type: Literal["FASTEST", "MINTRF"] | None = None
        first_last: int | None = None
        dept_time: str | None = None
        train_seq: int | None = None

    async def get_metro_route(self, params: QueryParams):
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(
                self.base_url, params=params.dict(exclude_none=True)
            ) as resp:
                res = await resp.json()
                return orjson.loads(res)

    async def get_dummy_metro_route(self, params: QueryParams):
        """공공데이터 포털 장애로 인한 임시 응답 데이터"""
        return [
            {
                "dept_station": "을지로3가역",
                "dest_station": "교대역",
                "linenum": "3",
            },
            {
                "dept_station": "교대역",
                "dest_station": "강남역",
                "linenum": "2",
            },
            {
                "dept_station": "강남역",
                "dest_station": "양재시민의숲역",
                "linenum": "신분당",
            },
        ]
