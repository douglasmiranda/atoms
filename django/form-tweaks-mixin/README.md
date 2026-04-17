# Django Form Tweaks Mixin

A small mixin to apply common Django form field tweaks automatically:

- Use field labels as placeholders for selected fields.
- Remove the default label suffix (colon).
- Add CSS classes to widgets by widget type.

## File

- `forms.py`: contains `FormTweaksMixin`.

## Usage

```python
from django import forms
from .forms import FormTweaksMixin


class ContactForm(FormTweaksMixin, forms.Form):
    tweak_label_as_placeholder = ("name", "email")
    tweak_remove_label_colon = True
    tweak_classes_for_widget = {
        forms.TextInput: "form-control",
        forms.EmailInput: "form-control",
        forms.Textarea: "form-control",
    }

    name = forms.CharField(label="Name")
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Message", widget=forms.Textarea)
```

## Notes

- Keep `FormTweaksMixin` before `forms.Form`/`forms.ModelForm` in class inheritance.
