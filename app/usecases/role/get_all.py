from logging import Logger
from app.dto.role import RoleDTOResponse
from app.dto.usecase_result import UsecaseResult, UsecaseStatus
from app.repository.role import RoleRepository


class GetAllRolesUsecase:
    def __init__(self, logger: Logger, repo: RoleRepository):
        self._logger = logger
        self._repo = repo

    async def execute(self) -> UsecaseResult:
        try:
            roles = await self._repo.get_all_roles()

            role_dtos = []
            for role in roles:
                role_dtos.append(
                    RoleDTOResponse(
                        id=role.id,
                        role=role.role,
                        permissions=role.permissions,
                    )
                )

            return UsecaseResult(data=role_dtos)
        except Exception as e:
            self._logger.error(f"get all roles error: {e}", exc_info=True)
            return UsecaseResult(UsecaseStatus.INTERNAL_ERROR, e)
