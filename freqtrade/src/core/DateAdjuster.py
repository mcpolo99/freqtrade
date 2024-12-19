# DateAdjuster.py
# import datetime
import logging
from dataclasses import field  # asdict, dataclass,
from datetime import datetime, timedelta, timezone
from enum import Enum

import pandas as pd


logger = logging.getLogger(__name__)


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


############ DATETIME ADJUSTMENT ############

"""DONE"""


class DateDirection(Enum):
    START = 0
    END = 1
    NEXT = 4
    PREVIOUS = 5
    CURRENT = 10
    NOW = 11


"""Done"""


def Get_Valid_DateTime(in_datetime: datetime, interval: str, direction: tuple) -> datetime:
    """
    Get the valid datetime (start or end) based on the provided direction
    ((START, END), (PREVIOUS,CURRENT,NEXT)).

    Parameters:
        in_symbol (str): The symbol for which to get the datetime (e.g., "BTCUSDT").
        in_datetime (str or datetime): The input datetime.
        interval (str): The interval (e.g., '1m', '15m', '1h', '1d').
        direction tuple(DateDirection,DateDirection): The direction for which to
        retrieve the datetime ((START, END), (PREVIOUS,CURRENT,NEXT)).

        IF first tuple is DateDirection.NOW and second whatever, we get utcnow()

    Returns:
        datetime: The valid start or end datetime for the asset.
    """
    interval_mappings = INTERVAL_MAPPINGS
    interval_duration = interval_mappings[interval]

    first, second = (
        direction
        # firs always need to be of DateDirection.START or END, and second can be
        # DateDirection.CURRENT / NEXT / PREVIOUS
    )

    in_datetime = pd.to_datetime(in_datetime)
    if first == DateDirection.NOW:
        return utcnow()
    # # Check if we need to get the start or end datetime based on the date_dir parameter.
    if first == DateDirection.START:
        in_datetime = _adjust_dateTime(in_datetime=in_datetime, interval=interval, direction=first)
    elif first == DateDirection.END:
        in_datetime = _adjust_dateTime(in_datetime=in_datetime, interval=interval, direction=first)
    else:
        logger.error(f"WRONG INPUT FOR FIRST {first}")

    if second == DateDirection.CURRENT:
        """Returns current in_datetime based on interval datetime"""
        return in_datetime
    elif second == DateDirection.NEXT:
        """Returns 'next' in_datetime """
        return in_datetime + interval_duration
    elif second == DateDirection.PREVIOUS:
        """Returns 'PREVIOUS' in_datetime """
        return in_datetime - interval_duration
    else:
        logger.error(f"WRONG INPUT FOR SECOND {second}")

    return None


"""DONE"""


def _adjust_dateTime(in_datetime: datetime, interval: str, direction: DateDirection):
    """
    Adjust the in_datetime to the beginning or end of the appropriate interval period.

    Parameters:
        in_datetime (datetime): The input datetime.
        interval (str): The interval (e.g., '1m', '15m', '1h', '1d').
        direction (int): Adjustment direction:
                        0 for start_datetime, 1 for end_datetime.

    Returns:
        datetime: Adjusted datetime based on interval and direction.
    """
    ##gets the UTC datetime

    # convert to datetime if not datetime object..
    if not isinstance(in_datetime, datetime):
        in_datetime = pd.to_datetime(in_datetime)

    if direction == DateDirection.START:  # Adjust to start of interval
        if interval.endswith("m"):  # Minute-based intervals
            minutes = int(interval[:-1])  # get how many minutes the interval holds..
            in_datetime = in_datetime.replace(second=0, microsecond=0)
            minutes_offset = in_datetime.minute % minutes
            in_datetime -= timedelta(minutes=minutes_offset)

        elif interval.endswith("h"):  # Hourly intervals
            hours = int(interval[:-1])
            in_datetime = in_datetime.replace(minute=0, second=0, microsecond=0)
            hours_offset = in_datetime.hour % hours
            in_datetime -= timedelta(hours=hours_offset)

        elif interval == "1d":  # Daily intervals
            in_datetime = in_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

        elif interval == "1w":  # Weekly intervals
            in_datetime -= timedelta(days=in_datetime.weekday())
            in_datetime = in_datetime.replace(hour=0, minute=0, second=0, microsecond=0)

        elif interval == "1M":  # Monthly intervals
            in_datetime = in_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        elif interval.endswith("d") and interval != "1d":  # Multi-day intervals
            """For some reason on my home pc i need to do minusval
            but on laptop i need no to do minusval"""
            days = int(interval[:-1])  # Extract the number of days in the interval
            in_datetime = in_datetime.replace(
                hour=0, minute=0, second=0, microsecond=0
            )  # Align to start of the day
            start_of_epoch = datetime(1970, 1, 1)  # Epoch start
            days_since_epoch = (in_datetime - start_of_epoch).days  # -1  # Total days since epoch

            # Calculate the offset for the interval
            days_offset = days_since_epoch % days
            minusval = days - days_offset  #
            if days_offset != 0:  # Adjust to the start of the previous interval
                in_datetime -= timedelta(days=minusval)

            # logger.debug("")

        # logger.debug(f"{interval} ST; dir: {direction.name}
        # now:{now}
        # before conv in_dt: {in_datetime} >
        # {self._adjust_to_previous_interval(in_datetime, interval)}") ##enable for debug log

    elif direction == DateDirection.END:  # Adjust to end of interval
        if interval.endswith("m"):  # Minute-based intervals
            minutes = int(interval[:-1])
            in_datetime = in_datetime.replace(second=0, microsecond=0)
            minutes_offset = in_datetime.minute % minutes
            end_of_interval = in_datetime + timedelta(minutes=(minutes - minutes_offset))
            in_datetime = end_of_interval - timedelta(milliseconds=1)

        elif interval.endswith("h"):  # Hourly intervals
            hours = int(interval[:-1])
            base_datetime = in_datetime.replace(minute=0, second=0, microsecond=0)
            hours_offset = base_datetime.hour % hours
            current_interval_end = base_datetime + timedelta(hours=(hours - hours_offset))
            in_datetime = current_interval_end - timedelta(milliseconds=1)

        elif interval == "1d":  # Daily intervals
            in_datetime = in_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
            in_datetime += timedelta(days=1) - timedelta(milliseconds=1)

        elif interval == "1w":  # Weekly intervals
            days_to_add = 6 - in_datetime.weekday()
            in_datetime = in_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
            in_datetime += timedelta(days=days_to_add + 1) - timedelta(milliseconds=1)

        elif interval == "1M":  # Monthly intervals
            next_month = in_datetime.month % 12 + 1
            year = in_datetime.year if next_month != 1 else in_datetime.year + 1
            end_of_month = in_datetime.replace(
                year=year, month=next_month, day=1, hour=0, minute=0, second=0, microsecond=0
            )
            in_datetime = end_of_month - timedelta(milliseconds=1)

        elif interval.endswith("d") and interval != "1d":  # Multi-day intervals
            """some very strange behaviour on this different pcs"""
            days = int(interval[:-1])
            in_datetime = in_datetime.replace(
                hour=23, minute=59, second=59, microsecond=00000
            ) + timedelta(milliseconds=999)  # worked on laptop
            # in_datetime = in_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
            start_of_epoch = datetime(1970, 1, 1)
            # Calculate days offset from the epoch
            days_since_epoch = (in_datetime - start_of_epoch).days - 1  # Total days since epoch
            # days_is_a_interval_day = (in_datetime - start_of_epoch).days % days
            # Calculate the offset for the interval
            days_offset = days_since_epoch % days

            # days_to_add_for_end = days-days_is_a_interval_day
            minusval = days - days_offset  #
            # if days_to_add_for_end != days:
            #     in_datetime += timedelta(days=minusval) #- timedelta(milliseconds=1)

            if days_offset != 0:  # Adjust to the start of the previous interval
                in_datetime += timedelta(days=minusval)

            # logger.debug("")
        else:
            logger.error(f"wrong direction provided: {direction}")

    return in_datetime


############ DATETIME ADJUSTMENT ############

VALID_INTERVALS: list[str] = field(
    default_factory=lambda: [
        "1m",
        "3m",
        "5m",
        "15m",
        "30m",
        "1h",
        "2h",
        "4h",
        "6h",
        "8h",
        "12h",
        "1d",
        "3d",
        "1w",
    ]
)


def generate_interval_mappings(time_intervals: list[str]) -> dict[str, timedelta]:
    """Generate interval mappings for valid time intervals."""
    mappings = {}
    for interval in time_intervals:
        if interval.endswith("m") and interval[-1].islower():  # Lowercase minutes
            value = int(interval[:-1])
            mappings[interval] = timedelta(minutes=value)
        elif interval.endswith("h"):  # Hours
            value = int(interval[:-1])
            mappings[interval] = timedelta(hours=value)
        elif interval.endswith("d"):  # Days
            value = int(interval[:-1])
            mappings[interval] = timedelta(days=value)
        elif interval.endswith("w"):  # Weeks
            value = int(interval[:-1])
            mappings[interval] = timedelta(weeks=value)
        elif interval.endswith("M") and interval[-1].isupper():  # Uppercase months
            value = int(interval[:-1])
            mappings[interval] = timedelta(days=value * 30)  # Approximation
        else:
            logger.warning(f"Invalid interval format: {interval}")
    return mappings


INTERVAL_MAPPINGS = generate_interval_mappings(VALID_INTERVALS)
