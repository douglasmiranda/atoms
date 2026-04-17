from django.forms import BaseInlineFormSet

from django import forms


class CustomInlineFormSet(BaseInlineFormSet):
    """Custom inline formset to add a custom delete button with Bootstrap styling.

    This formset overrides the `add_fields` method to customize the "DELETE" field.
    The custom delete button is styled with Bootstrap classes.

    Example usage:

    ```python
    from django.forms import inlineformset_factory
    from .models import ParentModel, ChildModel

    MyFormSet = inlineformset_factory(
        ParentModel,
        ChildModel,
        formset=CustomInlineFormSet,
        fields="__all__",
        extra=1,
    )
    ```
    """

    def add_fields(self, form, index):
        super().add_fields(form, index)
        # customizing for bootstrap needs
        if "DELETE" in form.fields:
            form.fields["DELETE"] = forms.BooleanField(
                label="Delete",
                widget=forms.CheckboxInput(attrs={"class": "btn-check"}),
                required=False,
            )
