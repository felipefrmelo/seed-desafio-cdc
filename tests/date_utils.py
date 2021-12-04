from datetime import date, timedelta, datetime


def make_publish_date(days_in_future=1):
    """
    Returns a date that is days in the future.
    """
    result = date.today() + timedelta(days=days_in_future)
    return result.__str__()


def make_expire_date(days_in_future=1):
    """
    Returns a date that is days in the future.
    """
    result = datetime.utcnow() + timedelta(days=days_in_future)
    return result.isoformat()
