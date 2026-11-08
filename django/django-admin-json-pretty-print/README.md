# Django Admin - Pretty Print (formatted / indented / no color) JSON (read-only)

Escape the JSON before marking it safe. `json.dumps` does not HTML-escape, so values containing `</pre>` or tags would otherwise break out of the `<pre>` and become XSS.

```python
import html
import json
from django.utils.safestring import mark_safe
from django.contrib import admin

from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    readonly_fields = ("pretty_metadata",)

    @admin.display(description="Meta Info")
    def pretty_metadata(self, publication):
        # publication.metadata is a JSONField
        pretty_json = json.dumps(publication.metadata, indent=4, sort_keys=True)
        return mark_safe(f"<pre>{html.escape(pretty_json)}</pre>")
```
