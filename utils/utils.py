"""Utility functions."""

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import REGISTRY
from prometheus_client.openmetrics.exposition import CONTENT_TYPE_LATEST
from prometheus_client.openmetrics.exposition import generate_latest
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from utils.config import DISABLE_TELEMETRY


def metrics(request: Request) -> Response:
    """Generate metrics for Prometheus."""
    return Response(
        generate_latest(REGISTRY), headers={"Content-Type": CONTENT_TYPE_LATEST}
    )


def setup_otlp(
    app: ASGIApp, app_name: str, endpoint: str, log_correlation: bool = True
) -> None:
    """Setting up OpenTelemetry."""
    # Setting OpenTelemetry
    # set the service name to show in traces
    resource = Resource.create(
        attributes={"service.name": app_name, "compose_service": app_name}
    )

    # set the tracer provider
    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)

    tracer.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))

    if log_correlation:
        LoggingInstrumentor().instrument(set_logging_format=True)

    if DISABLE_TELEMETRY:
        return

    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)
