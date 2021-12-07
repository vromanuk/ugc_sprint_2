import faust
import sentry_sdk
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware import Middleware

from src.api.routes import api_router
from src.core.config import get_settings

settings = get_settings()

sentry_sdk.init(dsn=settings.SENTRY_DNS, environment=settings.SENTRY_ENVIRONMENT)

middleware = [
    Middleware(SentryAsgiMiddleware),
]

app = FastAPI(
    version="1.0.0",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    middleware=[Middleware(SentryAsgiMiddleware)],
)

app.router.include_router(api_router, prefix=settings.API_PREFIX)


def get_faust_app() -> faust.App:
    return faust.App(
        settings.FAUST_PROJECT_NAME,
        broker=f"//{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
        topic_partitions=settings.DEFAULT_NUMBER_PARTITIONS,
    )
