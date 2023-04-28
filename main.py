from aiohttp import web
from config.config import Config
from app.handlers.middlewares import manage_session
from app.handlers.user import user_routes
from app.handlers.auth import auth_routes
from app.handlers.role import role_routes
from dotenv import load_dotenv


def create_app() -> web.Application:
    auth_handler = web.Application()
    auth_handler.add_routes(auth_routes)

    role_handler = web.Application(middlewares=[manage_session])
    role_handler.add_routes(role_routes)

    user_handler = web.Application(middlewares=[manage_session])
    user_handler.add_routes(user_routes)

    api = web.Application()
    api.add_subapp("/auth", auth_handler)
    api.add_subapp("/roles", role_handler)
    api.add_subapp("/users", user_handler)


    app = web.Application()
    app.add_subapp("/api/v1", api)

    return app

def run(app: web.Application) -> None:
    web.run_app(app, port=Config.APP_PORT)


if __name__ == "__main__":
    load_dotenv()
    app = create_app()
    run(app)


