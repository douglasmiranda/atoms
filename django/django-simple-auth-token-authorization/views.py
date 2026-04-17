from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .token import token_required


@require_http_methods(["GET", "HEAD"])
@token_required
def publications(request, *args, **kwargs):
    # Here you might want to add some rate limiting
    data = {"status": "ok"}
    return JsonResponse(data, status=200)
