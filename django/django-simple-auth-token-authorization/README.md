# Django Simple Auth Token Authorization

Simple token-based authorization for Django views using the `Authorization: Token <token>` header.

This snippet provides:

- a model to store API tokens (`APIToken`)
- a decorator to protect views (`@token_required`)
- a small example view (`publications`)

## Files

- `models.py`: `APIToken` model with token metadata and expiration.
- `token.py`: token generator and `token_required` decorator.
- `views.py`: protected sample endpoint.

## How it works

1. A token is created with `secrets.token_hex(32)` (64 hex chars).
2. The client sends `Authorization: Token <token>`.
3. The decorator validates header format and token shape.
4. It loads an active, non-expired token from DB and updates `last_used`.
5. It sets `request.user` from the token owner and calls the view.

## Setup

1. Add the model from `models.py` to your Django app.
2. Run migrations.
3. Copy `token.py` and update this line with your app label:

```python
APIToken = apps.get_model("MY-APP-CONTAINING-THE-MODEL-APIToken", "APIToken")
```

For example, if your app label is `api`:

```python
APIToken = apps.get_model("api", "APIToken")
```

4. Protect your views with `@token_required`.

## Usage

```python
# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .token import token_required


@require_http_methods(["GET", "HEAD"])
@token_required
def publications(request, *args, **kwargs):
    return JsonResponse({"status": "ok"}, status=200)
```

Add the URL route:

```python
# urls.py
from django.urls import path

from .views import publications

urlpatterns = [
    path("publications/", publications, name="publications"),
]
```

Create a token (example in Django shell):

```python
from django.contrib.auth import get_user_model
from your_app.models import APIToken

User = get_user_model()
user = User.objects.get(username="alice")
api_token = APIToken.objects.create(user=user, description="local test")
print(api_token.token)
```

Call protected endpoint:

```bash
curl -i \
	-H "Authorization: Token <TOKEN_VALUE>" \
	http://localhost:8000/publications/
```

## Error responses

The decorator returns HTTP `401` in these cases:

- Missing or malformed header:

```json
{
	"status": "error",
	"error": {
		"code": "token_required",
		"message": "Auth header missing or not in the format 'Token <token>'."
	}
}
```

- Invalid token format:

```json
{
	"status": "error",
	"error": {
		"code": "invalid_token",
		"message": "Invalid or malformed token."
	}
}
```

- Token not found, inactive, or expired:

```json
{
	"status": "error",
	"error": {
		"code": "expired_token",
		"message": "Invalid or expired token."
	}
}
```

## Notes

- `APIToken.user` is `OneToOneField`, so each user can have only one token.
- You might wanna choose how you will deal with default expiration if not set.
- The decorator expects 64-char lowercase/uppercase hex tokens. If you change the token generation method, make sure to update the validation logic in the decorator accordingly.
- Consider adding rate limiting to protected views to prevent abuse.
- This is a simple implementation. Depending on your needs, consider additional security measures like token revocation (here you could just delete or force expire tokens) and scopes/permissions.
