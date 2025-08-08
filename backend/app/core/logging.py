# backend/app/core/logging.py
import os
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

def init_sentry(app):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        release=os.getenv("SENTRY_RELEASE"),
        environment=os.getenv("SENTRY_ENVIRONMENT"),
    )
    app.add_middleware(SentryAsgiMiddleware)
