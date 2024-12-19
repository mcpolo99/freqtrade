import logging

from freqtrade.src.Loggers import setup_logging  # log_exception, log_table,


setup_logging()
logger = logging.getLogger(__name__)
print("Hello world")

logger.debug("FUCKNG TEAST")
