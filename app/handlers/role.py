from pydantic import ValidationError
from app.dto.role import RoleDTORequest
from app.dto.usecase_result import UsecaseStatus
from app.handlers.helpers.checks import is_permitted
from app.handlers.helpers.handle_failure_result import handle_failure_result
from app.handlers.helpers.responses import failure_response, success_response
from app.repository.role import RoleRepository
from aiohttp import web
from app.usecases.role.create import CreateRoleUsecase
from app.usecases.role.delete import DeleteRoleUsecase
from app.usecases.role.get_all import GetAllRolesUsecase
from app.usecases.role.get_by_id import GetRoleByIdUsecase
from app.usecases.role.update import UpdateRoleUsecase
from config.config import Config
from logger.logger import get_logger


role_routes = web.RouteTableDef()


@role_routes.post("/")
async def register(request):
    logger = get_logger(Config.LOG_LEVEL)

    role_repo = RoleRepository()
    create_role_usecase = CreateRoleUsecase(logger, role_repo)

    if not await is_permitted(request.session, "create_role"):
        return failure_response("access denied", 403)
    
    if not request.has_body:
        return failure_response("request must has body", 400)

    body = await request.json()
    try:
        role_dto = RoleDTORequest(
            role=body.get("role"),
            permissions=body.get("permissions"),
        )
    except ValidationError as e:
        return failure_response(e.errors(), 400)

    result = await create_role_usecase.execute(role_dto)

    if result.status != UsecaseStatus.SUCCESS:
        return handle_failure_result(result)
    else:
        return success_response()


@role_routes.get("/{id}")
async def get_role_by_id(request):
    try:
        id = int(request.match_info.get("id"))
    except ValueError:
        return failure_response("invalid url", 400)

    if not await is_permitted(request.session, "get_role_by_id"):
        return failure_response("access denied", 403)

    logger = get_logger(Config.LOG_LEVEL)

    role_repo = RoleRepository()
    get_role_by_id_usecase = GetRoleByIdUsecase(logger, role_repo)

    result = await get_role_by_id_usecase.execute(id)
    role_dto = result.data

    if result.status != UsecaseStatus.SUCCESS:
        return handle_failure_result(result)
    else:
        return success_response(role_dto.dict())


@role_routes.get("/")
async def get_all_roles(request):
    if not await is_permitted(request.session, "get_all_roles"):
        return failure_response("access denied", 403)

    logger = get_logger(Config.LOG_LEVEL)

    role_repo = RoleRepository()
    get_all_roles_usecase = GetAllRolesUsecase(logger, role_repo)

    result = await get_all_roles_usecase.execute()
    role_dtos = result.data

    role_dicts = []
    for dto in role_dtos:
        role_dicts.append(dto.dict())

    if result.status != UsecaseStatus.SUCCESS:
        return handle_failure_result(result)
    else:
        return success_response(role_dicts)


@role_routes.put("/{id}")
async def update_role(request):
    try:
        id = int(request.match_info.get("id"))
    except ValueError:
        return failure_response("invalid url", 400)

    if not await is_permitted(request.session, "update_role"):
        return failure_response("access denied", 403)

    logger = get_logger(Config.LOG_LEVEL)

    role_repo = RoleRepository()
    update_role_usecase = UpdateRoleUsecase(logger, role_repo)

    if not request.has_body:
        return failure_response("request must has body", 400)    

    body = await request.json()
    try:
        role_dto = RoleDTORequest(
            role=body.get("role"),
            permissions=body.get("permissions"),
        )
    except ValidationError as e:
        return failure_response(e.errors(), 400)

    result = await update_role_usecase.execute(id, role_dto)

    if result.status != UsecaseStatus.SUCCESS:
        return handle_failure_result(result)
    else:
        return success_response()


@role_routes.delete("/{id}")
async def delete_role(request):
    try:
        id = int(request.match_info.get("id"))
    except ValueError:
        return failure_response("invalid url", 400)

    if not await is_permitted(request.session, "delete_role"):
        return failure_response("access denied", 403)

    logger = get_logger(Config.LOG_LEVEL)

    role_repo = RoleRepository()
    delete_role_usecase = DeleteRoleUsecase(logger, role_repo)

    result = await delete_role_usecase.execute(id)

    if result.status != UsecaseStatus.SUCCESS:
        return handle_failure_result(result)
    else:
        return success_response()
