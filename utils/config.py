"""Config for api."""

import os

APP_NAME = os.environ.get("APP_NAME", "api")
EXPOSE_PORT = os.environ.get("EXPOSE_PORT", 8000)
OTLP_GRPC_ENDPOINT = os.environ.get("OTLP_GRPC_ENDPOINT", "http://tempo:4317")
DISABLE_TELEMETRY = os.environ.get("DISABLE_TELEMETRY", False)
