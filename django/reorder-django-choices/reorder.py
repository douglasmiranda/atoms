def reorder_choices(choices, choices_order):
    """
    Reorder your existing iterable of `choices` into a new one based on the
    provided `choices_order`.

    :param choices: Iterable of "choices".
        Usually a list of tuples like so: [('stored_value', "Display Value")]
    :param choices_order: List or tuple with the values in the wanted order.
        The values should be the 'stored_value' of the `choices` iterable.
        It can be provided as many values as needed, the rest that is not
        provided will be returned right after the provided order.
        Example: ('option-1', 'option-2')
    :return: list of tuples (list of choices)
    :rtype: list

    Useful for presenting the choices in forms and views.

    Basically:
        if `choices_order` is: ("c",)
        and `choices` is: [('a', "A"), ('b', "B"), ('c', "C")]
        this will be the result:
        [('c', "C"), ('a', "A"), ('b', "B")]

    It will reorder as many choices as provided in `choices_order`.
    The remaining choices will be displayed as they come, right after the ordered ones.

    - https://docs.djangoproject.com/en/6.0/ref/models/fields/#choices

    Usage::

    >>> choices_order = ("published", "editing")
    >>> choices = [
        ("archived", "Archived"),
        ("hold", "On Hold"),
        ("published", "Published"),
        ("editing", "Editing"),
        ("draft", "Draft"),
    ]
    >>> assert reorder_choices(choices, choices_order) == [
        ("published", "Published"),
        ("editing", "Editing"),
        ("archived", "Archived"),
        ("hold", "On Hold"),
        ("draft", "Draft"),
    ]
    >>> print(reorder_choices(choices, choices_order))
    [('published', 'Published'), ('editing', 'Editing'), ('archived', 'Archived'), ('hold', 'On Hold'), ('draft', 'Draft')]
    """
    ordered = []
    unordered = []
    for choice, display_text in choices:
        try:
            index = choices_order.index(choice)
        except ValueError:
            unordered.append((choice, display_text))
            continue

        ordered.insert(index, (choice, display_text))
    return ordered + unordered
