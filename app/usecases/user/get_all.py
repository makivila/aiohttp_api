from logging import Logger
from app.dto.usecase_result import UsecaseResult, UsecaseStatus
from app.dto.user import UserDTOResponse
from app.repository.user import UserRepository


class GetAllUsersUsecase:
    def __init__(self, logger: Logger, repo: UserRepository):
        self._logger = logger
        self._repo = repo

    async def execute(self) -> UsecaseResult:
        try:
            users = await self._repo.get_all_users()

            user_dtos = []
            for user in users:
                user_dtos.append(
                    UserDTOResponse(
                        id=user.id,
                        first_name=user.first_name,
                        second_name=user.second_name,
                        login=user.login,
                        born=user.born,
                        registration_date=user.registration_date,
                        role_id=user.role_id,
                    )
                )

            return UsecaseResult(data=user_dtos)
        except Exception as e:
            self._logger.error(f"get all users error: {e}", exc_info=True)
            return UsecaseResult(UsecaseStatus.INTERNAL_ERROR, e)
