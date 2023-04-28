import logging
from os import environ as env


class Config:
    APP_PORT = env["APP_PORT"]

    LOG_LEVEL = logging.INFO

    DB_USERNAME = env["DB_USERNAME"]
    DB_PASSWORD = env["DB_PASSWORD"]
    DB_DATABASE_NAME = env["DB_DATABASE_NAME"]
    DB_HOST = env["DB_HOST"]
    DB_PORT = env["DB_PORT"]

    SESSION_EXPIRES_DAYS = 7
