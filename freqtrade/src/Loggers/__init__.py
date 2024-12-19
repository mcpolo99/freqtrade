import datetime
import logging
import logging.handlers
from pathlib import Path

from freqtrade.src.Loggers.colorformater import ColoredFormatter
from freqtrade.src.Loggers.set_log_levels import set_loggers
from freqtrade.src.Loggers.stream_handler import Stream_Handler


# '%(asctime)s | %(module)s:$(lineno)s:%(funcName)s | %(levelname)s | %(message)s'
LOG_FILE_FORMAT = logging.Formatter(
    "%(asctime)s | %(filename)s:%(lineno)d:%(funcName)s | %(levelname)s | %(message)s"
)
LOG_CONSOLE_FORMAT = ColoredFormatter(
    "%(asctime)s | %(filename)s:%(lineno)d:%(funcName)s | %(levelname)s | %(message)s"
)

LOG_DIR = "./Logs/"
LOG_FILE = LOG_DIR + datetime.datetime.today().strftime("%Y-%m-%d") + ".log"


formatter = logging.Formatter()


def get_existing_handlers(handlertype):
    """
    Returns Existing handler or None (if the handler has not yet been added to the root handlers).
    """
    return next((h for h in logging.root.handlers if isinstance(h, handlertype)), None)


def setup_logging() -> None:
    """
    Setup logging for both console and file outputs.
    """
    # Set root logger level
    logging.root.setLevel(logging.DEBUG)

    # File logger setup
    handler_rf = get_existing_handlers(logging.handlers.RotatingFileHandler)
    if handler_rf:
        logging.root.removeHandler(handler_rf)

    try:
        logfile_path = Path(LOG_FILE)
        logfile_path.parent.mkdir(parents=True, exist_ok=True)
        handler_rf = logging.handlers.RotatingFileHandler(
            filename=logfile_path, maxBytes=1024 * 1024 * 10, backupCount=10
        )
    except PermissionError as e:
        logging.error(f"PermissionError: Unable to create log file. {e}")
        return  # Exit gracefully if file can't be created

    handler_rf.setFormatter(LOG_FILE_FORMAT)
    logging.root.addHandler(handler_rf)

    # Console logger setup
    handler_sr = get_existing_handlers(Stream_Handler)
    if handler_sr:
        logging.root.removeHandler(handler_sr)

    handler_sr = Stream_Handler()
    handler_sr.setFormatter(LOG_CONSOLE_FORMAT)
    logging.root.addHandler(handler_sr)

    set_loggers(verbosity=0, api_verbosity="info")


@staticmethod
def log_table(data=None, headers=None, level=logging.INFO):
    """
    Example inputs:

        data = [
            ["ID", "Name", "Age"],  # Headers
            [
                [1, "Alice", 30],        # Row 1
                [2, "Bob", 25],          # Row 2
                [3, "Charlie", 35]       # Row 3
            ]
        ]
        wILL RETURN:
        +------+---------+-------+
        |   ID | Name    |   Age |
        +======+=========+=======+
        |    1 | Alice   |    30 |
        +------+---------+-------+


        data = [
            [1, "Alice", 30],
            [2, "Bob", 25],
            [3, "Charlie", 35]
        ]
        Will return :
        +------------+------------+------------+
        |   Column 1 | Column 2   |   Column 3 |
        +============+============+============+
        |          1 | Alice      |         30 |
        +------------+------------+------------+
    """
    import pandas as pd
    from tabulate import tabulate  # For table formatting

    # If the first element is a list of headers
    if isinstance(data, list) and len(data) == 2 and isinstance(data[1][0], list):
        if isinstance(data[0], list):
            headers = data[0]  # First element is headers
            data = data[1]  # Remaining elements are the data

    # If no headers are provided and data is a list of lists, use the keys of the first dict as headers
    elif headers is None and isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
        headers = [f"Column {i+1}" for i in range(len(data[0]))]

    elif isinstance(data, pd.DataFrame):
        headers = "keys"
        data = data
    elif isinstance(data, pd.Series):
        headers = "keys"
        data = data.to_frame().T

    # Ensure headers and data are not None
    if headers is None or data is None:
        logging.log(level, "Headers or data not provided, or wrong format")
        return

    # Create a formatted grid from the data using tabulate
    table = tabulate(tabular_data=data, headers=headers, tablefmt="grid")
    # Log the table at the specified level
    stacklevel = get_stacklevel()
    logging.log(level, f"\n\r{table}\n\r", stacklevel=stacklevel)


@staticmethod
def log_exception(e):
    import sys
    import traceback

    # Get the traceback details
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback_details = traceback.format_exception(exc_type, exc_value, exc_tb)

    # Get the file and line number from the traceback
    file_name, line_number, _, _ = traceback.extract_tb(exc_tb)[-1]

    # Determine the correct stack level dynamically
    stacklevel = get_stacklevel()

    # Log the exception details
    # logging.error(f"Exception occurred in file: {file_name}, line: {line_number}", stacklevel=stacklevel-1)
    logging.error(f"Error: {e}", stacklevel=stacklevel - 1)
    logging.error("".join(traceback_details), stacklevel=stacklevel - 1)  # Log the full traceback


@staticmethod
def get_stacklevel() -> int:
    """
    Determines the correct stacklevel dynamically by inspecting the call stack.
    """
    import inspect

    # Get the current call stack
    stack = inspect.stack()

    # Check for the level where the function was called from, and adjust based on context
    for i, frame in enumerate(stack):
        # Check if the function is a logging call and not one of our helper methods
        if frame.function not in ("log_table", "loggException", "get_stacklevel"):
            # We skip the current function and the helper methods and return the correct stack level
            return i + 1  # Add 1 to account for the level above

    # Fallback to 1 if no suitable stack level is found
    return 1


# logger = logging.getLogger(__name__)
# logger1 = logging.getLogger("TEST")
# # USE TO DEBUG HERE ONLY LOCAL FILE
# # Main function
# def main():
#     # print(__name__)
#     # setup_logging()
#     setup_logging()

#     logger.info("heheheh")
#     logger1.info("logger2")


#     headers = ["ID", "Name", "Age"]
#     data = [

#         [1, "Alice", 30],
#         [2, "Bob", 25],
#         [3, "Charlie", 35]
#     ]
#     data2 = [
#         ["ID", "Name", "Age"],
#         [
#             [1, "Alice", 30],
#             [2, "Bob", 25],
#             [3, "Charlie", 35],
#         ]
#     ]
#     log_table(data2)
#     try:
#         raise Exception("TESRT")
#     except Exception as e:
#         loggException(e)


#     # ints = range(1000)

#     # for i in ints:
#     #     logger1.info(f"ino {i}")


# if __name__ == "__main__":
#     main()
