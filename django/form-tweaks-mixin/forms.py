class FormTweaksMixin:
    """
    Mixin to apply tweaks to form fields, such as using labels as placeholders,
    removing label colons, and adding CSS classes to widgets.

    To use this mixin, define the following class attributes in your form:
    - `tweak_label_as_placeholder`: A tuple of field names for which the label should be used as a placeholder.
    - `tweak_remove_label_colon`: A boolean indicating whether to remove the colon from field labels.
    - `tweak_classes_for_widget`: A dictionary mapping widget types to CSS class names to be added to those widgets.

    Example usage:
    ```python
    class MyForm(FormTweaksMixin, forms.Form):
        tweak_label_as_placeholder = ("name", "email")
        tweak_remove_label_colon = True
        tweak_classes_for_widget = {forms.TextInput: "form-control"}

        name = forms.CharField(label="Name")
        email = forms.EmailField(label="Email")
    ```
    """

    tweak_label_as_placeholder = tuple()
    tweak_remove_label_colon = False
    tweak_classes_for_widget = dict()

    def make_placeholder(self, field_name):
        self.fields[field_name].widget.attrs.update({
            "placeholder": self.fields[field_name].label
        })

    def make_classes_for_widget(self, field_name):
        for widget_type, css_class in self.tweak_classes_for_widget.items():
            if isinstance(self.fields[field_name].widget, widget_type):
                self.fields[field_name].widget.attrs.update({"class": css_class})

    def __init__(self, *args, **kwargs):
        if self.tweak_remove_label_colon:
            kwargs["label_suffix"] = ""

        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name in self.tweak_label_as_placeholder:
                self.make_placeholder(field_name)

            self.make_classes_for_widget(field_name)
