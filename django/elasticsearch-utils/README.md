# Elasticsearch date range helpers (Django)

Small helpers to build timezone-aware `gte` / `lte` bounds from `datetime.date` values, and optional `elasticsearch-dsl` range filters for multi-date search.

Useful when your UI sends calendar dates but your index stores datetimes on a field like `created`.

## Functions

### `ensure_max_datetime(date, max_datetime_allowed=None) -> datetime`

Converts a date to end-of-day in the active Django timezone. If that datetime is after `max_datetime_allowed`, returns the cap instead.

- `max_datetime_allowed` defaults to `timezone.now()` (so “today” does not extend past the current moment).

```python
from datetime import date, datetime
from search_utils import ensure_max_datetime

ensure_max_datetime(date(2026, 5, 31))
# -> 2026-05-31 23:59:59.999999 (aware)

ensure_max_datetime(
    date(2026, 5, 31),
    datetime(2026, 5, 31, 14, 0, 0, tzinfo=...),
)
# -> capped at 2026-05-31 14:00:00
```

### `make_range_datetime_filter(start, end) -> dict[str, datetime]`

Builds inclusive bounds for one range:

- `gte`: start of `start` (00:00:00)
- `lte`: end of `end` (23:59:59.999999), via `ensure_max_datetime`

```python
from datetime import date
from search_utils import make_range_datetime_filter

make_range_datetime_filter(date(2026, 5, 31), date(2026, 6, 1))
# {"gte": ..., "lte": ...}
```

### `my_collection_multiple_date_filters(dates) -> list[ESQFilter]`

One `range` filter per date, each covering that full day on the `created` field. Empty `dates` returns `[]`.

Adapt the field name (`created`) or function name to match your index.

```python
from datetime import date
from search_utils import my_collection_multiple_date_filters

my_collection_multiple_date_filters([
    date(2026, 5, 31),
    date(2026, 6, 1),
])
# [
#   Q("range", created={"gte": ..., "lte": ...}),  # May 31 only
#   Q("range", created={"gte": ..., "lte": ...}),  # Jun 1 only
# ]
```

## Usage with elasticsearch-dsl

### Single date range

```python
from datetime import date
from elasticsearch.dsl import Q, Search
from search_utils import make_range_datetime_filter

bounds = make_range_datetime_filter(date(2026, 5, 1), date(2026, 5, 31))
search = Search(index="my_collection").filter("range", created=bounds)
```

### Multiple selected days (OR)

When the user picks several individual days, combine day filters with `bool` / `should`:

```python
from datetime import date
from elasticsearch.dsl import Search
from search_utils import my_collection_multiple_date_filters

dates = [date(2026, 5, 31), date(2026, 6, 1)]
day_filters = my_collection_multiple_date_filters(dates)

search = Search(index="my_collection").filter(
    "bool",
    should=day_filters,
    minimum_should_match=1,
)
```

### Form / query params

```python
# request.GET: start=2026-05-01&end=2026-05-31
start = date.fromisoformat(request.GET["start"])
end = date.fromisoformat(request.GET["end"])
bounds = make_range_datetime_filter(start, end)
```

## Notes

- `ensure_max_datetime` avoids querying “future” time on the end date when the cap is `now()` (typical for “through today” filters).
- `my_collection_multiple_date_filters` is an example tied to the `created` field; copy and rename for other indices or fields.

