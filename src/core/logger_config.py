from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "custom_json_formatter": {
            "format": "{'time':'%(asctime)s', 'logger_name': '%(name)s', 'level': '%(levelname)s', 'message': '%(message)s', 'filename': '%(filename)s', 'funcName': '%(funcName)s', 'lineno': '%(lineno)s'}"
        }
    },
    "handlers": {
        "stream_handler": {
            "formatter": "custom_json_formatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "uvicorn": {"handlers": ["stream_handler"], "level": "INFO", "propagate": 0},
        "uvicorn.error": {"handlers": ["stream_handler"], "level": "INFO",  "propagate": 0},
        "uvicorn.access": {"handlers": ["stream_handler"], "level": "INFO", "propagate": 0},
        "root": {"handlers": ["stream_handler"], "level": "INFO", "propagate": 0},
    }
}


def init_logger() -> None:
    dictConfig(LOGGING_CONFIG)
