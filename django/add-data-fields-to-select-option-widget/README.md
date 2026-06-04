# Add Data Attributes to Select Option Widget

A custom `forms.Select` widget that adds `data-*` attributes to individual `<option>` elements.

Useful when the browser needs extra metadata per choice (for example, toggling other fields with JavaScript, styling, or client-side validation) without embedding that data in the visible label.

## File

- `forms.py`: contains `DataAttributesSelectOptions`.

## Widget signature

```python
DataAttributesSelectOptions(attrs=None, choices=(), data=None)
```

- `attrs`: extra attributes for the `<option>` elements (not the `<select>` element).
- `choices`: standard Django choice tuples `(value, label)`.
- `data`: dict mapping **choice value** → dict of attribute names and values (without the `data-` prefix).

Rendered output prefixes keys with `data-`. Only options whose value exists in `data` get extra attributes.

## Example output

```python
from forms import DataAttributesSelectOptions

choices = (
    (1, "Choice 1"),
    (2, "Choice 2"),
)
data = {1: {"foo": "foo"}, 2: {"bar": "bar"}}

widget = DataAttributesSelectOptions(choices=choices, data=data)
widget.render("name", 1)
```

```html
<select name="name">
  <option value="1" selected data-foo="foo">Choice 1</option>
  <option value="2" data-bar="bar">Choice 2</option>
</select>
```

## Usage

### On a `ChoiceField`

```python
from django import forms
from .forms import DataAttributesSelectOptions

PLAN_CHOICES = (
    ("basic", "Basic"),
    ("pro", "Pro"),
)

PLAN_DATA = {
    "basic": {"price": "9", "seats": "1"},
    "pro": {"price": "29", "seats": "10"},
}


class SignupForm(forms.Form):
    plan = forms.ChoiceField(
        choices=PLAN_CHOICES,
        widget=DataAttributesSelectOptions(
            choices=PLAN_CHOICES,
            data=PLAN_DATA,
        ),
    )
```

### In a `ModelForm` (values from the database)

```python
from django import forms
from .forms import DataAttributesSelectOptions
from .models import Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("product",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        products = Product.objects.all()
        choices = [(p.pk, p.name) for p in products]
        data = {
            p.pk: {"sku": p.sku, "stock": str(p.stock)}
            for p in products
        }

        self.fields["product"].widget = DataAttributesSelectOptions(
            choices=choices,
            data=data,
        )
        self.fields["product"].choices = choices
```

### Reading attributes in the browser

```html
<select id="id_plan" name="plan">
  <option value="basic" data-price="9" data-seats="1">Basic</option>
  <option value="pro" data-price="29" data-seats="10">Pro</option>
</select>
```

```javascript
const select = document.getElementById("id_plan");

select.addEventListener("change", () => {
  const option = select.selectedOptions[0];
  const price = option.dataset.price;
  const seats = option.dataset.seats;
  // update UI from data-price / data-seats
});
```

## Notes

- Choice values in `data` must match the type used in `choices` (for example, `1` vs `"1"`).
- Attributes are only added when the option value is a key in `data`; other options render normally.
- Keys in the inner dict are turned into `data-{key}` on the `<option>`.
- Reference: https://docs.djangoproject.com/en/6.0/ref/forms/widgets/
