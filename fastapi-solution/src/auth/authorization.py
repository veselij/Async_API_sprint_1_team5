from fastapi.security.http import HTTPBearer
from orjson import JSONDecodeError
from starlette.requests import Request
import httpx
from core import config


class TokenCheck(HTTPBearer):

    def __init__(self, auto_error: bool = False) -> None:
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> list:
        credentials = await super().__call__(request)
        if not credentials:
            return []
        token = credentials.credentials
        roles = await self.send_request_to_auth(token)
        return roles

    async def send_request_to_auth(self, token: str) -> list:
        async with httpx.AsyncClient() as client:
            response = await client.post(config.AUTH_URL, json={"access_token": token})
            try:
                result = response.json()
            except JSONDecodeError:
                result = []
        return result
