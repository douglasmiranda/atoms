from datetime import date


class DateConverter:
    """
    For urls in urls.py.

    A Django URL converter for dates in the format yyyy-mm-dd.
    This converter will parse a date string in the format yyyy-mm-dd and convert it to a Python date object.
    It can also convert a date object back to a string in the same format for URL reversing.
    Example usage in urls.py:
        from django.urls import path, register_converter
        from .converters import DateConverter
        register_converter(DateConverter, 'date')
        urlpatterns = [
            path('events/<date:date>/', views.event_detail, name='event_detail'),
        ]
    This will allow you to use URLs like /events/2023-10-01/ and have the date passed as a Python date object to your view.
    """

    # yyyy-mm-dd (zero-padded month/day)
    regex = r"\d{4}-\d{2}-\d{2}"

    def to_python(self, value: str):
        year, month, day = map(int, value.split("-"))
        try:
            return date(year, month, day)
        except ValueError as exc:
            raise ValueError("invalid date") from exc

    def to_url(self, value):  # for reverse()
        return value.strftime("%Y-%m-%d")
