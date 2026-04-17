import secrets
from enum import UNIQUE, StrEnum, verify
from functools import wraps

from django.apps import apps
from django.http import JsonResponse
from django.utils import timezone


def gen_token():
    """Generate a secure random token."""
    # https://docs.python.org/3/library/secrets.html
    # Maybe you want to use a different method to generate tokens
    # If you change this, make sure to update the token field in the model accordingly
    # Also change the validation in the token_required decorator
    return secrets.token_hex(32)


@verify(UNIQUE)
class Errors(StrEnum):
    TOKEN_REQUIRED = "token_required"
    INVALID_TOKEN = "invalid_token"
    EXPIRED_TOKEN = "expired_token"


def token_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header or not auth_header.startswith("Token "):
            return JsonResponse(
                {
                    "status": "error",
                    "error": {
                        "code": Errors.TOKEN_REQUIRED,
                        "message": "Auth header missing or not in the format 'Token <token>'.",
                    },
                },
                status=401,
            )

        token = auth_header.split(" ")[1]

        # Validate token format
        # Depends on gen_token implementation
        if len(token) != 64 or not all(c in "0123456789abcdef" for c in token.lower()):
            return JsonResponse(
                {
                    "status": "error",
                    "error": {
                        "code": Errors.INVALID_TOKEN,
                        "message": "Invalid or malformed token.",
                    },
                },
                status=401,
            )

        APIToken = apps.get_model("MY-APP-CONTAINING-THE-MODEL-APIToken", "APIToken")

        try:
            api_token = APIToken.objects.select_related("user").get(
                token=token, is_active=True, expires_at__gt=timezone.now()
            )
        except APIToken.DoesNotExist:
            return JsonResponse(
                {
                    "status": "error",
                    "error": {
                        "code": Errors.EXPIRED_TOKEN,
                        "message": "Invalid or expired token.",
                    },
                },
                status=401,
            )

        api_token.last_used = timezone.now()
        api_token.save(update_fields=["last_used"])

        request.user = api_token.user
        return view_func(request, *args, **kwargs)

    return wrapper
