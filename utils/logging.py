"""Set up logging for api."""

import logging
from logging import config as logging_config

logger = logging.getLogger("api")


class EndpointFilter(logging.Filter):
    """Filters out the metrics endpoint from logs."""

    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter method for the endpoint filter."""
        return record.getMessage().find("GET /metrics") == -1


LOGGING_DEFAULTS = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "root": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.access": {
            "handlers": ["grafana_access_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
        "gunicorn": {"handlers": ["default"]},
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
        },
        "grafana_access_handler": {
            "formatter": "grafana_access",
            "class": "logging.StreamHandler",
        },
    },
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "grafana_access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s",
        },
    },
}


def setup_logging(log_level: int) -> None:
    """Set up logging.

    Args:
        log_level (int): The log level from the logging library
    """
    logging_config.dictConfig(LOGGING_DEFAULTS)
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

    for name in logging.root.manager.loggerDict.keys():
        if any(
            substring in name
            for substring in [
                "transformers",
                "dill",
            ]
        ):
            logging.getLogger(name).setLevel(logging.ERROR)
        else:
            logging.getLogger(name).setLevel(log_level)
