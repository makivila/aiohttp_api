from logging import Logger
from app.dto.usecase_result import UsecaseResult, UsecaseStatus
from app.dto.user import LoginDTO
from app.repository.user import UserRepository


class LoginUsecase:
    def __init__(self, logger: Logger, repo: UserRepository):
        self._logger = logger
        self._repo = repo

    async def execute(self, login_dto: LoginDTO) -> UsecaseResult:
        try:
            user = await self._repo.get_user_by_login(login_dto.login)

            if not user:
                return UsecaseResult(
                    UsecaseStatus.UNAUTHORIZED,
                    "user with such login not found",
                )

            if login_dto.password != user.password:
                return UsecaseResult(UsecaseStatus.UNAUTHORIZED, "incorrect password")

            return UsecaseResult(data={"user_id": user.id})
        except Exception as e:
            self._logger.error(f"login error: {e}", exc_info=True)
            return UsecaseResult(UsecaseStatus.INTERNAL_ERROR, e)
