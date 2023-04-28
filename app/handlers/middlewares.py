import datetime
from aiohttp import web
from app.handlers.helpers.responses import failure_response
from app.managers.session import SessionManager
from config.config import Config


@web.middleware
async def manage_session(request, handler):
    session_manager = SessionManager()
    session_id = request.cookies.get("session_id")
    if not session_id:
        return failure_response(
            "unauthorized: there is no session_id in the cookie", 401
        )

    session = await session_manager.get_session_by_id(session_id)
    if not session:
        return failure_response(
            "unauthorized: session with such session_id not found", 401
        )

    if session.last_activity < (
        datetime.datetime.now() - datetime.timedelta(Config.SESSION_EXPIRES_DAYS)
    ):
        return failure_response("unauthorized: session expired, login required", 401)

    request.session = session

    response = await handler(request)

    # do not set session if user deleted himself
    if request.get("user_deleted"):
        return response

    new_session_id = await session_manager.set_session(session.user_id)
    response.set_cookie("session_id", new_session_id)

    return response
