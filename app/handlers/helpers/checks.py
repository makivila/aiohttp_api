from app.models.models import Session


async def is_permitted(session: Session, route_name: str) -> bool:
    permissions = session.user.role.permissions

    if "*" in permissions:
        return True

    return route_name in permissions
