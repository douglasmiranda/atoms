from dataclasses import dataclass
from datetime import datetime

# This is basically a draft
# it works, it's just very simplistic
# looks for a single occurrence; match; return
# The main goal it's just parse the date and have control of
# the format I matched.
# Example: read autocomplete field and trigger a search when
# the search term match at least the dd/mm (%d/%m) format.
# if format_key == "day_month": search database for day month
# if format_key == "day_month_year": search database for day month year


def extract_date(text, formats=None):
    """Try to parse a date from a string given a list of formats.
    >>> extract_date("22/06")
    >>> extract_date.<locals>.Date(day=22, month=6, year=1900, format_key='day_month')

    >>> date = extract_date("22/06")

    >>> date.day
    >>> 22

    >>> date.month
    >>> 6

    >>> date.year
    >>> 1900

    >>> date.date()
    >>> datetime.date(1900, 6, 22)

    >>> date.format_key
    >>> 'day_month'

    >>> if date and date.format_key == "day_month":
            print("filter by day and month only")
    filter by day and month only
    """

    @dataclass
    class Date:
        day: int
        month: int
        year: int = None
        format_key: str = None

        def date(self):
            return datetime(self.year, self.month, self.day).date()

    if not formats:
        formats = {"day_month": "%d/%m", "day_month_year": "%d/%m/%Y"}

    for key in formats.keys():
        normalized = text.strip()
        fmt = formats[key]

        if "%Y" not in fmt and "%y" not in fmt and "%G" not in fmt:
            # Parse with an explicit leap year to avoid ambiguous no-year parsing.
            sentinel_year = 2000
            try:
                date = datetime.strptime(f"{normalized};{sentinel_year}", f"{fmt};%Y")
            except ValueError:
                continue

            year = 1900
            if date.month == 2 and date.day == 29:
                year = sentinel_year
            return Date(date.day, date.month, year, key)

        try:
            date = datetime.strptime(normalized, fmt)
        except ValueError:
            continue

        return Date(date.day, date.month, date.year, key)
    return None


if __name__ == "__main__":
    date = extract_date("22/06")
    assert date is not None
    assert date.day == 22
    assert date.month == 6
    assert date.year == 1900
    assert date.format_key == "day_month"
    assert str(date.date()) == "1900-06-22"

    date = extract_date("29/02")
    assert date is not None
    assert date.day == 29
    assert date.month == 2
    assert date.year == 2000
    assert date.format_key == "day_month"
    assert str(date.date()) == "2000-02-29"

    date = extract_date("22/06/2026")
    assert date is not None
    assert date.day == 22
    assert date.month == 6
    assert date.year == 2026
    assert date.format_key == "day_month_year"
    assert str(date.date()) == "2026-06-22"

    custom_formats = {
        "iso": "%Y-%m-%d",
        "day_month_year": "%d/%m/%Y",
    }
    date = extract_date("2026-04-16", formats=custom_formats)
    assert date is not None
    assert date.format_key == "iso"
    assert str(date.date()) == "2026-04-16"

    assert extract_date("invalid") is None
