from logging import Logger
from app.dto.usecase_result import UsecaseResult, UsecaseStatus
from app.dto.role import RoleDTOResponse
from app.repository.role import RoleRepository


class GetRoleByIdUsecase:
    def __init__(self, logger: Logger, repo: RoleRepository):
        self._logger = logger
        self._repo = repo

    async def execute(self, id: int) -> UsecaseResult:
        try:
            role = await self._repo.get_role_by_id(id)

            if not role:
                return UsecaseResult(UsecaseStatus.NOT_FOUND)

            role_dto = RoleDTOResponse(
                id=role.id,
                role=role.role,
                permissions=role.permissions,
            )

            return UsecaseResult(data=role_dto)
        except Exception as e:
            self._logger.error(f"get role by id error: {e}", exc_info=True)
            return UsecaseResult(UsecaseStatus.INTERNAL_ERROR, e)
