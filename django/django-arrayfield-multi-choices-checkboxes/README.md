# Django (postgres) ArrayField Multiple Choices as checkboxes

```python
from django import forms
from django.contrib.postgres.fields import ArrayField


class MultipleChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
            "widget": forms.CheckboxSelectMultiple,
            **kwargs,
        }
        return super(ArrayField, self).formfield(**defaults)

    def to_python(self, value):
        res = super().to_python(value)
        if isinstance(res, list):
            value = [self.base_field.to_python(val) for val in res]
        return value
```

Check [fields.py](fields.py) and [models.py](models.py) for example usage.

You may wanna do that kinda of thing in forms manipulations instead of directly in the model, but this was my use case.