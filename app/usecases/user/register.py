import datetime
from logging import Logger
from app.dto.usecase_result import UsecaseResult, UsecaseStatus
from app.dto.user import UserDTORequest
from app.models.models import User
from app.repository.role import RoleRepository
from app.repository.user import UserRepository


class RegisterUsecase:
    def __init__(
        self,
        logger: Logger,
        user_repo: UserRepository,
        role_repo: RoleRepository,
    ):
        self._logger = logger
        self._user_repo = user_repo
        self._role_repo = role_repo

    async def execute(self, user_dto: UserDTORequest) -> UsecaseResult:
        try:
            user_exists = await self._user_repo.get_user_by_login(user_dto.login)

            if user_exists:
                return UsecaseResult(
                    UsecaseStatus.BAD_REQUEST,
                    "user with such login already registered",
                )

            role = await self._role_repo.get_role_by_role_name(user_dto.role)

            new_user = User(
                first_name=user_dto.first_name,
                second_name=user_dto.second_name,
                login=user_dto.login,
                password=user_dto.password,
                born=user_dto.born,
                registration_date=datetime.datetime.now(),
                role_id=role.id,
            )

            await self._user_repo.create_user(new_user)

            return UsecaseResult()
        except Exception as e:
            self._logger.error(f"register error: {e}", exc_info=True)
            return UsecaseResult(UsecaseStatus.INTERNAL_ERROR, e)
