from http.client import HTTPException
import httpx
from fastapi.security.http import HTTPBearer
from orjson import JSONDecodeError
from starlette.requests import Request

from core import config
from core.decorators import backoff_async
from core.exceptions import RetryExceptionError


class TokenCheck(HTTPBearer):
    def __init__(self, auto_error: bool = False) -> None:
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> list:
        credentials = await super().__call__(request)
        if not credentials:
            return []
        token = credentials.credentials
        user_roles_resonse = await self.send_request_to_auth(token)
        if user_roles_resonse is None:
            return []
        return user_roles_resonse

    @backoff_async(
        config.logger,
        start_sleep_time=0.1,
        factor=2,
        border_sleep_time=10,
        max_retray=2,
    )
    async def send_request_to_auth(self, token: str) -> list:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    config.AUTH_URL, json={"access_token": token}
                )
            except httpx.ReadTimeout:
                raise RetryExceptionError("Auth server not available")
            result = response.json()
            if response.status_code in (
                httpx.codes.UNPROCESSABLE_ENTITY,
                httpx.codes.UNAUTHORIZED,
            ):
                raise HTTPException(response.status_code, detail=result)
        return result
