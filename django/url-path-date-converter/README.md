# Django URL Path Date Converter

A tiny Django path converter for ISO-like dates in the format `YYYY-MM-DD`.

It lets Django URL patterns parse incoming date segments into `datetime.date` objects, and format `date` objects back to strings for URL reversing.

## File

- `dates.py`: contains `DateConverter`.

## Converter behavior

- Accepted URL format: `YYYY-MM-DD` (zero-padded month/day).
- `to_python("2026-04-16")` returns a `datetime.date(2026, 4, 16)`.
- Invalid calendar dates (for example `2026-02-30`) raise `ValueError("invalid date")`.
- `to_url(date(2026, 4, 16))` returns `"2026-04-16"`.

## Usage

Put `DateConverter` somewhere importable (for example in `converters.py`):

```python
# converters.py
from .dates import DateConverter
```

Register it in your URL config:

```python
# urls.py
from django.urls import path, register_converter
from . import views
from .dates import DateConverter

register_converter(DateConverter, "date")

urlpatterns = [
    path("events/<date:event_date>/", views.event_detail, name="event_detail"),
]
```

Use it in a view:

```python
# views.py
from django.http import HttpResponse


def event_detail(request, event_date):
    # event_date is a datetime.date instance
    return HttpResponse(f"Event date: {event_date.isoformat()}")
```

Reverse URLs with a `date` object:

```python
from datetime import date
from django.urls import reverse

url = reverse("event_detail", kwargs={"event_date": date(2026, 4, 16)})
assert url == "/events/2026-04-16/"
```

## Notes

- Due to how these url path parsing works in Django, if the date is invalid, the request it's not gonna even touch the view, but instead will return a 404 Not Found response.
- This converter validates both format and real calendar dates.
- If you only need matching and not conversion, a plain regex path can be enough.
- Reference: https://docs.djangoproject.com/en/6.0/topics/http/urls/#registering-custom-path-converters
