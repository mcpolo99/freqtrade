import logging
import subprocess
import sys
import time

# import os
from pathlib import Path

# import cmd2
# from cmd2 import style
# from cmd2.ansi import Bg, Fg
from freqtrade.src.Loggers import setup_logging  # log_exception, log_table,


setup_logging()
logger = logging.getLogger(__name__)


# Add a main entry point
def main():
    # try:
    # Get the directory of the current script (main.py)
    script_dir = Path(__file__)
    script_dir = script_dir.parent
    commandDownload = [
        "freqtrade",
        "download-data",
        "--pairs",
        "DOGE/USDT",
        "BTC/USDT",
        "-t",
        "15m",
        "30m",
        "1h",
        "2h",
        "--prepend",
        "--timerange",
        "20100101-",
    ]
    CommandTrade = ["freqtrade", "trade", "-s", "WaveTrendMACDStrategy"]

    subprocess.run(CommandTrade)
    # Construct the full path to the other script
    another_script_path = Path(script_dir, "test.py")
    # result = subprocess.run(["python", another_script_path], capture_output=True, text=True)
    # Run the script and allow interaction
    # subprocess.run(["python", "freqtrade"])
    # subprocess.run(["python", another_script_path])

    # while True:
    #     time.sleep(3)
    #     logger.debug(f"heeej")


# except KeyboardInterrupt:
#     logger.info("interupted")
# finally:
#     sys.exit()


if __name__ == "__main__":
    main()
