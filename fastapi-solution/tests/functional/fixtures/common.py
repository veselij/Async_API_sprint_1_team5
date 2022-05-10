import aiohttp
import asyncio
from dataclasses import dataclass
from multidict import CIMultiDictProxy
import pytest
from typing import Optional



@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
async def web_client():
    web_client = aiohttp.ClientSession()
    yield web_client
    await web_client.close()


@pytest.fixture
def make_get_request(web_client):
    async def inner(url: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        async with web_client.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
