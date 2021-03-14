from pprint import pprint

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from src.apps.organization import views as organization
from src.settings import Configuration

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

settings = Configuration()

print('Settings loaded:\n', '---' * 23)
pprint(settings.dict())

app = FastAPI(
    debug=settings.DEBUG, title=settings.PROJECT_NAME,
    version=settings.VERSION, default_response_class=ORJSONResponse,
)
if app.debug is False:
    sentry_sdk.init(dsn=settings.SENTRY_DSN)
    asgi_app = SentryAsgiMiddleware(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# app.include_router(auth.router)
app.include_router(organization.router)
