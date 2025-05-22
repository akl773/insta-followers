from datetime import datetime, time
from zoneinfo import ZoneInfo

IST_TZ = ZoneInfo("Asia/Kolkata")


def get_morning_time():
    """
    Returns the current date at 00:00:00 (midnight) in IST timezone.
    """

    now_ist = datetime.now(IST_TZ)
    # Create a new datetime with the same date but time set to midnight (00:00:00)
    midnight_ist = datetime.combine(now_ist.date(), time(0, 0, 0), tzinfo=IST_TZ)

    return midnight_ist
