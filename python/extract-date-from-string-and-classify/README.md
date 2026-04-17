# Extract Date From String And Classify

Parse a date string and return both the parsed value and which format matched.

This is useful when the matched format controls what kind of filtering to do (for example, day/month search vs full date search).

## File

- `extract.py`: contains `extract_date(text, formats=None)`.

## Function signature

```python
extract_date(text, formats=None) -> Date | None
```

- `text`: input string to parse (leading/trailing spaces are ignored).
- `formats`: optional dict where key is a label and value is a `datetime.strptime` format.

If `formats` is not provided, it defaults to:

```python
{
    "day_month": "%d/%m",
    "day_month_year": "%d/%m/%Y",
}
```

## Return value

Returns a `Date` dataclass instance with:

- `day`
- `month`
- `year`
- `format_key`: the dict key for the matched format

And helper method:

- `date()`: returns `datetime.date(year, month, day)`

Returns `None` if no format matches.

## Example

```python
from extract import extract_date

date = extract_date("22/06")

assert date is not None
assert date.day == 22
assert date.month == 6
assert date.year == 1900
assert date.format_key == "day_month"
assert str(date.date()) == "1900-06-22"
```

## Classify By Matched Format

```python
from extract import extract_date

value = extract_date("22/06")

if value and value.format_key == "day_month":
    print("filter by day and month")
elif value and value.format_key == "day_month_year":
    print("filter by exact day/month/year")
else:
    print("invalid input")
```

## Custom Formats

```python
from extract import extract_date

formats = {
    "iso": "%Y-%m-%d",
    "br_full": "%d/%m/%Y",
}

value = extract_date("2026-04-16", formats=formats)

assert value is not None
assert value.format_key == "iso"
assert str(value.date()) == "2026-04-16"
```

## Notes

- Parsing is strict: the whole input must match one of the provided formats.
- Only one match is returned: the first matching format in dict iteration order.
- For `%d/%m`, Python uses year `1900` by default.
