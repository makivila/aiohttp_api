from logging import Logger
from app.dto.usecase_result import UsecaseResult, UsecaseStatus
from app.repository.role import RoleRepository


class DeleteRoleUsecase:
    def __init__(self, logger: Logger, repo: RoleRepository):
        self._logger = logger
        self._repo = repo

    async def execute(self, id: int) -> UsecaseResult:
        try:
            user = await self._repo.get_role_by_id(id)

            if not user:
                return UsecaseResult(UsecaseStatus.NOT_FOUND)

            await self._repo.delete_role(id)

            return UsecaseResult()
        except Exception as e:
            self._logger.error(f"delete role error: {e}", exc_info=True)
            return UsecaseResult(UsecaseStatus.INTERNAL_ERROR, e)
