from pydantic import ValidationError
from app.dto.usecase_result import UsecaseStatus
from app.dto.user import UserDTORequest
from app.handlers.helpers.checks import is_permitted
from app.handlers.helpers.handle_failure_result import handle_failure_result
from app.handlers.helpers.responses import failure_response, success_response
from app.repository.role import RoleRepository
from app.repository.user import UserRepository
from app.usecases.user.delete import DeleteUserUsecase
from app.usecases.user.get_all import GetAllUsersUsecase
from app.usecases.user.get_by_id import GetUserByIdUsecase
from aiohttp import web
from app.usecases.user.update import UpdateUserUsecase
from config.config import Config
from logger.logger import get_logger


user_routes = web.RouteTableDef()


@user_routes.get("/{id}")
async def get_user_by_id(request):
    try:
        id = int(request.match_info.get("id"))
    except ValueError:
        return failure_response("invalid url", 400)

    if not await is_permitted(request.session, "get_user_by_id"):
        return failure_response("access denied", 403)

    if request.session.user_id != id and request.session.user.role.role != "admin":
        return failure_response("access denied", 403)

    logger = get_logger(Config.LOG_LEVEL)

    user_repo = UserRepository()
    get_user_by_id_usecase = GetUserByIdUsecase(logger, user_repo)

    result = await get_user_by_id_usecase.execute(id)
    user_dto = result.data

    if result.status != UsecaseStatus.SUCCESS:
        return handle_failure_result(result)
    else:
        return success_response(user_dto.dict())


@user_routes.get("/")
async def get_all_users(request):
    if not await is_permitted(request.session, "get_all_users"):
        return failure_response("access denied", 403)

    logger = get_logger(Config.LOG_LEVEL)

    user_repo = UserRepository()
    get_all_users_usecase = GetAllUsersUsecase(logger, user_repo)

    result = await get_all_users_usecase.execute()
    user_dtos = result.data

    user_dicts = []
    for dto in user_dtos:
        user_dicts.append(dto.dict())

    if result.status != UsecaseStatus.SUCCESS:
        return handle_failure_result(result)
    else:
        return success_response(user_dicts)


@user_routes.put("/{id}")
async def update_user(request):
    try:
        id = int(request.match_info.get("id"))
    except ValueError:
        return failure_response("invalid url", 400)

    if not await is_permitted(request.session, "update_user"):
        return failure_response("access denied", 403)

    if request.session.user_id != id and request.session.user.role.role != "admin":
        return failure_response("access denied", 403)

    logger = get_logger(Config.LOG_LEVEL)

    user_repo = UserRepository()
    role_repo = RoleRepository()
    update_user_usecase = UpdateUserUsecase(logger, user_repo, role_repo)

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
        if not request.session.user.role.role == "admin":
            return failure_response(
                "only admin permitted to set admin role to another user", 403
            )
    result = await update_user_usecase.execute(id, user_dto)

    if result.status != UsecaseStatus.SUCCESS:
        return handle_failure_result(result)
    else:
        return success_response()


@user_routes.delete("/{id}")
async def delete_user(request):
    try:
        id = int(request.match_info.get("id"))
    except ValueError:
        return failure_response("invalid url", 400)

    if not await is_permitted(request.session, "delete_user"):
        return failure_response("access denied", 403)

    if request.session.user_id != id and request.session.user.role.role != "admin":
        return failure_response("access denied", 403)

    logger = get_logger(Config.LOG_LEVEL)

    user_repo = UserRepository()
    delete_user_usecase = DeleteUserUsecase(logger, user_repo)

    result = await delete_user_usecase.execute(id)

    if result.status != UsecaseStatus.SUCCESS:
        return handle_failure_result(result)
    else:
        if request.session.user_id == id:
            request["user_deleted"] = True

        return success_response()
