import logging


logger = logging.getLogger(__name__)


def set_loggers(verbosity: int = 0, api_verbosity: str = "info") -> None:
    """
    Set the logging level for third party libraries
    :param verbosity: Verbosity level.
    :return: None
    """
    for logger_name in ("requests", "urllib3", "httpcore"):
        logging.getLogger(logger_name).setLevel(logging.INFO if verbosity <= 1 else logging.DEBUG)

    logging.getLogger("ccxt.base.exchange").setLevel(
        logging.INFO if verbosity <= 2 else logging.DEBUG
    )

    logging.getLogger("binace.client").setLevel(logging.INFO if verbosity <= 2 else logging.DEBUG)

    logging.getLogger("telegram").setLevel(logging.INFO)

    logging.getLogger("httpx").setLevel(logging.WARNING)

    logging.getLogger("werkzeug").setLevel(
        logging.ERROR if api_verbosity == "error" else logging.INFO
    )
