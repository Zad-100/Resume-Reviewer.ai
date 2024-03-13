import logging
import logging.config
import os


# Macros and constants
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
LOGS_FILE = os.path.join(LOGS_DIR, "app.log")
with open(LOGS_FILE, "w") as f:
    pass

# Logging Config
# More on Logging Configuration
# https://docs.python.org/3/library/logging.config.html
# Setting up a config
LOGGING_DEFAULT_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": """%(asctime)s \
- %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s""",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(message)s"},
    },
    "root": {"level": "DEBUG"},
}


def configure_logger(
    logger: logging.Logger = None,  # type: ignore
    cfg: dict = None,  # type: ignore
    log_file: str = LOGS_FILE,  # type: ignore
    console: bool = True,  # type: ignore
    log_level: str = "DEBUG"
) -> logging.Logger:
    """Function to setup configurations of logger through function."""

    if not cfg:
        cfg = LOGGING_DEFAULT_CONFIG
    logging.config.dictConfig(cfg)

    logger = logger or logging.getLogger()

    if log_file or console:
        for hdlr in logger.handlers:
            logger.removeHandler(hdlr)

        if log_file:
            fh = logging.FileHandler(log_file)
            fh.setLevel(getattr(logging, log_level))
            fh.setFormatter(
                logging.Formatter(
                    cfg['formatters']['default']['format'],
                    datefmt=cfg['formatters']['default']['datefmt']
                )
            )
            logger.addHandler(fh)

        if console:
            sh = logging.StreamHandler()
            sh.setLevel(getattr(logging, log_level))
            sh.setFormatter(
                logging.Formatter(
                    cfg['formatters']['default']['format'],
                    datefmt=cfg['formatters']['default']['datefmt']
                )
            )
            logger.addHandler(sh)

    return logger