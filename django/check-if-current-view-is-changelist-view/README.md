# Check If Current View Is Django Admin Changelist

A small helper to detect whether the current Django admin request is the changelist view for the current `ModelAdmin`.

Useful when you want to apply logic only on the list page (for example, optimize queryset fields).

## File

- `admin.py`: contains `is_changelist_view(model_admin_instance, request)`.

## Function signature

```python
is_changelist_view(model_admin_instance, request) -> bool
```

- `model_admin_instance`: current `admin.ModelAdmin` instance (`self` inside admin methods).
- `request`: current `HttpRequest`.

## How it works

It compares the current resolved URL name with Django admin's changelist naming pattern:

```python
f"{opts.app_label}_{opts.model_name}_changelist"
```

where `opts` comes from `model_admin_instance.opts`.

## Usage

```python
from django.contrib import admin
from .admin import is_changelist_view
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if is_changelist_view(self, request):
            # Only load fields needed for list display
            return queryset.only("title")

        return queryset
```

## Notes

- This helper is specific to Django admin URL naming conventions.
- It works when `request.resolver_match` is available (standard Django request cycle).
- You can adapt the suffix check pattern for other admin views (`_change`, `_delete`, etc.).
- Reference: https://docs.djangoproject.com/en/6.0/ref/contrib/admin/
