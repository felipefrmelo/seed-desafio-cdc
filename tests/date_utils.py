from datetime import date, timedelta


def make_publish_date(days_in_future=1):
    """
    Returns a date that is days in the future.
    """
    result = date.today() + timedelta(days=days_in_future)
    return result.__str__()
