import dateparser
from datetime import datetime


_ERR_DEHUMANIZATION_FAILED = '"{textual_duration}" n\'est pas une durée valide.'


def textual_duration_to_seconds(textual_duration: str) -> float:
    """
    Convert a textual duration such as "1min and 42 seconds" into seconds.

    Args:
        textual_duration (str): The human readable duration.

    Returns:
        float: The converted duration in seconds.
    """

    # TODO One issue here, is that absolute date like "2023/01/01" would be accepted, should be restricted to duration
    # TODO Fix debug msg "No localtime found"
    relative_base = datetime.now()
    future_date = dateparser.parse(
        textual_duration, settings={"RELATIVE_BASE": relative_base}
    )
    # in case textutal_duration is absolute, it can be in the past. # TODO I had to reverse the condition (<= with >) I have no idea why
    if (not future_date) or future_date > relative_base:
        raise ValueError(
            _ERR_DEHUMANIZATION_FAILED.format(textual_duration=textual_duration)
        )
    duration_sec = (relative_base - future_date).total_seconds()
    return duration_sec
