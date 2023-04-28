from logging import Logger
from app.dto.role import RoleDTORequest
from app.dto.usecase_result import UsecaseResult, UsecaseStatus
from app.models.models import Role
from app.repository.role import RoleRepository


class CreateRoleUsecase:
    def __init__(self, logger: Logger, repo: RoleRepository):
        self._logger = logger
        self._repo = repo

    async def execute(self, role_dto: RoleDTORequest) -> UsecaseResult:
        try:
            role_exists = await self._repo.get_role_by_role_name(role_dto.role)

            if role_exists:
                return UsecaseResult(
                    UsecaseStatus.BAD_REQUEST,
                    "such role already exists",
                )

            new_role = Role(
                role=role_dto.role,
                permissions=role_dto.permissions,
            )

            await self._repo.create_role(new_role)

            return UsecaseResult()
        except Exception as e:
            self._logger.error(f"create role error: {e}", exc_info=True)
            return UsecaseResult(UsecaseStatus.INTERNAL_ERROR, e)
