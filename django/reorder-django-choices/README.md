# Reorder Django Choices

Reorder an existing iterable of Django-like choices according to a preferred order of stored values.

Useful when you want a custom display order in forms/admin while keeping your original choices declaration simple.

## File

- `reorder.py`: contains `reorder_choices(choices, choices_order)`.

## Function signature

```python
reorder_choices(choices, choices_order) -> list[tuple]
```

- `choices`: iterable of `(stored_value, display_text)` tuples.
- `choices_order`: list/tuple with stored values in the desired order.

## Behavior

- Choices listed in `choices_order` are moved to the beginning, preserving that requested order.
- Any choice not listed in `choices_order` is appended after the ordered ones, preserving original relative order.
- Values present in `choices_order` but missing from `choices` are ignored.

## Example

```python
from reorder import reorder_choices

choices_order = ("published", "editing")
choices = [
    ("archived", "Archived"),
    ("hold", "On Hold"),
    ("published", "Published"),
    ("editing", "Editing"),
    ("draft", "Draft"),
]

result = reorder_choices(choices, choices_order)

assert result == [
    ("published", "Published"),
    ("editing", "Editing"),
    ("archived", "Archived"),
    ("hold", "On Hold"),
    ("draft", "Draft"),
]
```

## Django usage example

```python
STATUS_CHOICES = [
    ("draft", "Draft"),
    ("hold", "On Hold"),
    ("published", "Published"),
    ("archived", "Archived"),
]

STATUS_CHOICES = reorder_choices(STATUS_CHOICES, ("published", "draft"))
```

## Notes

- This helper expects each choice item to unpack as `(value, label)`.
- Typical Django choices use unique stored values. If values are repeated, ordering behavior may be surprising.
- Reference: https://docs.djangoproject.com/en/6.0/ref/models/fields/#choices
