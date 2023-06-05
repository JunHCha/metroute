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

    async def get_route(self, params: QueryParams):
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.get(
                self.base_url, params=params.dict(exclude_none=True)
            ) as resp:
                res = await resp.json()
                return orjson.loads(res)
