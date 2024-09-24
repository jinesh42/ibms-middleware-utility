from datetime import datetime


def check_if_min_even(datetime_str):
    dt = datetime.fromisoformat(datetime_str)
    current_minute = dt.minute
    if current_minute % 2 == 0:
        return 1
    else:
        return 0
