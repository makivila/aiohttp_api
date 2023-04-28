from aiohttp import web
from pydantic import ValidationError
from app.dto.usecase_result import UsecaseStatus
from app.dto.user import LoginDTO, UserDTORequest
from app.handlers.helpers.handle_failure_result import handle_failure_result
from app.handlers.helpers.responses import failure_response, success_response
from app.managers.session import SessionManager
from app.repository.role import RoleRepository
from app.repository.user import UserRepository
from app.usecases.user.login import LoginUsecase
from app.usecases.user.register import RegisterUsecase
from config.config import Config
from logger.logger import get_logger
from database.database import engine


auth_routes = web.RouteTableDef()


@auth_routes.post("/login")
async def login(request):
    session_manager = SessionManager(engine)
    logger = get_logger(Config.LOG_LEVEL)

    user_repo = UserRepository(engine)
    login_usecase = LoginUsecase(logger, user_repo)

    if not request.has_body:
        return failure_response("request must has body", 400)

    body = await request.json()
    try:
        login_dto = LoginDTO(
            login=body.get("login"),
            password=body.get("password"),
        )
    except ValidationError as e:
        return failure_response(e.errors(), 400)

    result = await login_usecase.execute(login_dto)

    if result.status != UsecaseStatus.SUCCESS:
        return handle_failure_result(result)

    session_id = await session_manager.set_session(result.data["user_id"])

    response = success_response()
    response.set_cookie("session_id", session_id)

    return response


@auth_routes.post("/register")
async def register(request):
    logger = get_logger(Config.LOG_LEVEL)

    user_repo = UserRepository(engine)
    role_repo = RoleRepository(engine)
    register_usecase = RegisterUsecase(logger, user_repo, role_repo)

    if not request.has_body:
        return failure_response("request must has body", 400)

    body = await request.json()
    try:
        user_dto = UserDTORequest(
            first_name=body.get("first_name"),
            second_name=body.get("second_name"),
            login=body.get("login"),
            password=body.get("password"),
            born=body.get("born"),
            role=body.get("role"),
        )
    except ValidationError as e:
        return failure_response(e.errors(), 400)

    if user_dto.role == "admin":
        if not await _is_requester_admin(request):
            return failure_response(
                "only admin permitted to register another admin", 403
            )

    result = await register_usecase.execute(user_dto)

    if result.status != UsecaseStatus.SUCCESS:
        return handle_failure_result(result)
    else:
        return success_response()


async def _is_requester_admin(request) -> bool:
    session_manager = SessionManager(engine)
    session_id = request.cookies.get("session_id")
    if not session_id:
        return False

    session = await session_manager.get_session_by_id(session_id)
    if not session:
        return False

    return session.role == "admin"
