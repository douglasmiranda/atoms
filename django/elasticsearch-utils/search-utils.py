from datetime import datetime

from django.utils import timezone
from elasticsearch.dsl import Q as ESQFilter


def ensure_max_datetime(
    date: datetime.date, max_datetime_allowed: datetime.datetime | None = None
) -> datetime.datetime:
    """Ensure the end-of-day datetime for a date does not exceed the allowed maximum.

    Args:
        date: Date to convert to end-of-day datetime.
        max_datetime_allowed: Maximum allowed datetime. Defaults to `timezone.now()` when omitted.
    Returns:
        datetime: End-of-day datetime, or the allowed maximum if that would be later.

    Example:
        ensure_max_datetime(datetime.date(2026, 5, 31))
        -> datetime(2026, 5, 31, 23, 59, 59)

    Example:
        ensure_max_datetime(datetime.date(2026, 5, 31), datetime.datetime(2026, 5, 31, 14, 00, 00))
        -> datetime(2026, 5, 31, 14, 00, 00)
    """
    if max_datetime_allowed is None:
        max_datetime_allowed = timezone.now()

    max_datetime = timezone.make_aware(datetime.combine(date, datetime.max.time()))
    if max_datetime > max_datetime_allowed:
        return max_datetime_allowed
    return max_datetime


def make_range_datetime_filter(
    start: datetime.date, end: datetime.date
) -> dict[str, datetime.datetime]:
    """Build a date range filter dict for Elasticsearch.

    Args:
        start: Start date (inclusive, start of day).
        end: End date (inclusive, end of day, clamped with `ensure_max_datetime`).
    Returns:
        dict[str, datetime.datetime]: Range filter with `gte` and `lte` bounds.

    Example:
        make_range_datetime_filter(datetime.date(2026, 5, 31), datetime.date(2026, 6, 1))
        -> {"gte": datetime(2026, 5, 31, 0, 0), "lte": datetime(2026, 6, 1, 23, 59, 59)}
    """
    start_date = timezone.make_aware(datetime.combine(start, datetime.min.time()))
    end_date = ensure_max_datetime(end)
    return {"gte": start_date, "lte": end_date}


def my_collection_multiple_date_filters(dates: list[datetime.date]) -> list[ESQFilter]:
    """Build date filters for the My Collection index in Elasticsearch.

    Args:
        dates: List of dates.
    Returns:
        list[ESQFilter]: List of date filters.

    Example:
        publications_multiple_date_filters([datetime.date(2026, 5, 31), datetime.date(2026, 6, 1)])
        [ESQFilter("range", created={"gte": datetime(2026, 5, 31, 0, 0), "lte": datetime(2026, 5, 31, 23, 59, 59)}),
         ESQFilter("range", created={"gte": datetime(2026, 6, 1, 0, 0), "lte": datetime(2026, 6, 1, 23, 59, 59)})]
    """
    if not dates:
        return []

    date_filters = []
    for date in dates:
        _filter = make_range_datetime_filter(start=date, end=date)
        # each date filter in the list looks like this:
        # ESQFilter("range", created={"gte": datetime(2026, 5, 31, 0, 0), "lte": datetime(2026, 5, 31, 23, 59, 59)})
        date_filters.append(ESQFilter("range", created=_filter))
    return date_filters
