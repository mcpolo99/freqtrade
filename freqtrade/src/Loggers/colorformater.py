import logging

from colorama import Fore, Style  # , Back


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to log levels and other parts of the log record."""

    COLOR_MAP = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.RED,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }

    RESET = Style.RESET_ALL

    def format(self, record):
        # Apply color to the log level
        color = self.COLOR_MAP.get(record.levelno, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"

        # Apply yellow color to the function name
        if record.funcName:
            record.funcName = f"{Fore.LIGHTYELLOW_EX}{record.funcName}{self.RESET}"
        if record.filename:
            record.filename = f"{Fore.GREEN}{record.filename}{self.RESET}"
        # if record.filename:
        #     record.filename = f"{Fore.GREEN}{record.filename}{self.RESET}"
        # if record.asctime:
        #     record.asctime = f"{Fore.RED}{record.asctime}{self.RESET}"

        # Apply color to the message itself (optional)
        record.message = f"{Fore.WHITE}{record.getMessage()}{self.RESET}"

        # Apply color to other log fields if desired (e.g., time, filename)
        formatted_log = super().format(record)

        return formatted_log
