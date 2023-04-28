from logging import Logger
from app.dto.usecase_result import UsecaseResult, UsecaseStatus
from app.dto.user import UserDTORequest
from app.repository.role import RoleRepository
from app.repository.user import UserRepository


class UpdateUserUsecase:
    def __init__(
        self,
        logger: Logger,
        user_repo: UserRepository,
        role_repo: RoleRepository,
    ):
        self._logger = logger
        self._user_repo = user_repo
        self._role_repo = role_repo

    async def execute(self, id: int, user_dto: UserDTORequest) -> UsecaseResult:
        try:
            user = await self._user_repo.get_user_by_id(id)

            if not user:
                return UsecaseResult(UsecaseStatus.NOT_FOUND)

            role = await self._role_repo.get_role_by_role_name(user_dto.role)

            user.first_name = user_dto.first_name
            user.second_name = user_dto.second_name
            user.login = user_dto.login
            user.password = user_dto.password
            user.born = user_dto.born
            user.role_id = role.id

            await self._user_repo.update_user(user)

            return UsecaseResult()
        except Exception as e:
            self._logger.error(f"update user error: {e}", exc_info=True)
            return UsecaseResult(UsecaseStatus.INTERNAL_ERROR, e)
