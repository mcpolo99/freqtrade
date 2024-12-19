import sys
from logging import StreamHandler


# from Loggers.colorFormater import ColoredFormatter


class Stream_Handler(StreamHandler):
    """"""

    def __init__(self):
        super().__init__(sys.stdout)

    def flush(self):
        """
        Override Flush behaviour - we keep half of the configured capacity
        otherwise, we have moments with "empty" logs.
        """
        self.acquire()
        try:
            sys.stderr.flush()
        finally:
            self.release()

    def emit(self, record):
        try:
            msg = self.format(record)
            # Don't keep a reference to stderr - this can be problematic with progressbars.
            sys.stderr.write(msg + "\n")
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)
