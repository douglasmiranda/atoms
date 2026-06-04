from django import forms


class DataAttributesSelectOptions(forms.Select):
    def __init__(self, attrs=None, choices=(), data=None):
        """Initialize the select widget with choices and data attributes.

        Args:
            attrs: Additional attributes for the select widget.
            choices: A tuple of choices for the select widget.
            data: A dictionary mapping option value -> data attributes.

        Example:
        >>> choices = (
        ...     (1, "Choice 1"),
        ...     (2, "Choice 2"),
        ... )
        >>> data = {1: {"foo": "foo"}, 2: {"bar": "bar"}}
        >>> widget = DataAttributesSelectOptions(choices=choices, data=data)
        >>> widget.render("name", 1)
        `'<select name="name"><option value="1" data-foo="foo">Choice 1</option><option value="2" data-bar="bar">Choice 2</option></select>'`

        Important notes about data attributes:
        - The data attributes are prefixed with "data-" by default.
        - The data attributes are only added to the option if the value is in the data dictionary.
        - The data key that points to the choice is type sensitive. Meaning it must match the type.
          For example:
            >>> choices = (
            ...     (1, "Choice 1"), # 1 is int
            ... )
            >>> data = {1: {"foo": "foo"}} # key 1 must also be int
        """
        super().__init__(attrs, choices)
        # mapping of option value -> data attributes
        self.data = data or {}

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        # Call the base method to get the standard option context
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )

        # Add custom data attributes if they exist for this value
        if value in self.data:
            for key, val in self.data[value].items():
                option["attrs"][f"data-{key}"] = val

        return option
