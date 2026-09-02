from pathlib import Path
import logging
import structlog
from structlog.stdlib import BoundLogger


def configure_logger(log_path: Path | None = None) -> BoundLogger:
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.format_exc_info,
        (
            structlog.processors.JSONRenderer(indent=2)
            if log_path
            else structlog.processors.KeyValueRenderer(
                key_order=["event", "level", "timestamp"]
            )
        ),
    ]

    wrapper_class = structlog.make_filtering_bound_logger(logging.INFO)

    if log_path:
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(message)s"))
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(handler)

    structlog.configure(
        processors=processors,
        wrapper_class=wrapper_class,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


def get_logger() -> BoundLogger:
    return structlog.get_logger()
