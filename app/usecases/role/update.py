from logging import Logger
from app.dto.usecase_result import UsecaseResult, UsecaseStatus
from app.dto.role import RoleDTORequest
from app.repository.role import RoleRepository


class UpdateRoleUsecase:
    def __init__(self, logger: Logger, repo: RoleRepository):
        self._logger = logger
        self._repo = repo

    async def execute(self, id: int, role_dto: RoleDTORequest) -> UsecaseResult:
        try:
            role = await self._repo.get_role_by_id(id)

            if not role:
                return UsecaseResult(UsecaseStatus.NOT_FOUND)

            role.role = role_dto.role
            role.permissions = role_dto.permissions

            await self._repo.update_role(role)

            return UsecaseResult()
        except Exception as e:
            self._logger.error(f"update role error: {e}", exc_info=True)
            return UsecaseResult(UsecaseStatus.INTERNAL_ERROR, e)
