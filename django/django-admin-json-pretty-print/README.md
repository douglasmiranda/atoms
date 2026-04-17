# Django Admin - Pretty Print (formatted / idented / no color) JSON (read-only)

**IMPORTANT:** Do not do this if your JSON is untrusted.

From [python docs](https://docs.python.org/3/library/json.html):

> Warning Be cautious when parsing JSON data from untrusted sources. A malicious JSON string may cause the decoder to consume considerable CPU and memory resources. Limiting the size of data to be parsed is recommended.

```python
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
        return mark_safe(f"<pre>{pretty_json}</pre>")
```

PS: I also have not tested the interaction between the JSON containing html tags and the `mark_safe` function.