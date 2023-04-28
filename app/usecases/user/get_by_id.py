from logging import Logger
from app.dto.usecase_result import UsecaseResult, UsecaseStatus
from app.dto.user import UserDTOResponse
from app.repository.user import UserRepository


class GetUserByIdUsecase:
    def __init__(self, logger: Logger, repo: UserRepository):
        self._logger = logger
        self._repo = repo

    async def execute(self, id: int) -> UsecaseResult:
        try:
            user = await self._repo.get_user_by_id(id)

            if not user:
                return UsecaseResult(UsecaseStatus.NOT_FOUND)

            user_dto = UserDTOResponse(
                id=user.id,
                first_name=user.first_name,
                second_name=user.second_name,
                login=user.login,
                born=user.born,
                registration_date=user.registration_date,
                role_id=user.role_id,
            )

            return UsecaseResult(data=user_dto)
        except Exception as e:
            self._logger.error(f"get user by id error: {e}", exc_info=True)
            return UsecaseResult(UsecaseStatus.INTERNAL_ERROR, e)
