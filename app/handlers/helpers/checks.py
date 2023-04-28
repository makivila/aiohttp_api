from app.models.models import Session


async def is_permitted(session: Session, route_name: str) -> bool:
    if "*" in session.permissions:
        return True

    return route_name in session.permissions
