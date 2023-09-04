def logger_conf(debug: bool = False) -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)-6s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "to_stderr": {
                "formatter": "default",
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            }
        },
        "root": {
            "level": "DEBUG" if debug else "INFO",
            "handlers": [
                "to_stderr"
            ]
        },
    }
