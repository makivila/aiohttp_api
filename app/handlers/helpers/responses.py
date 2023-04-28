import json
from typing import Any
from aiohttp import web


def success_response(data: Any = None) -> web.Response:
    if data:
        json_str = json.dumps(
            {"status": "success", "data": data}, default=str
        )  # for correct encoding date types
        return web.json_response(text=json_str)
    else:
        return web.json_response({"status": "success"})


def failure_response(message: str, status_code: int) -> web.Response:
    return web.json_response(
        {"status": "failure", "message": message},
        status=status_code,
    )
