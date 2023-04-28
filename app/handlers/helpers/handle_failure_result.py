from app.dto.usecase_result import UsecaseResult, UsecaseStatus
from app.handlers.helpers.responses import failure_response
from aiohttp import web


def handle_failure_result(result: UsecaseResult) -> web.Response:
    if result.status == UsecaseStatus.INTERNAL_ERROR:
        return failure_response(f"internal error: {result.data}", 500)
    elif result.status == UsecaseStatus.BAD_REQUEST:
        return failure_response(f"bad request: {result.data}", 400)
    elif result.status == UsecaseStatus.UNAUTHORIZED:
        return failure_response(f"unauthorized: {result.data}", 401)
    elif result.status == UsecaseStatus.NOT_FOUND:
        return failure_response(f"resource not found", 404)
    else:
        return failure_response("unknown error", 500)
