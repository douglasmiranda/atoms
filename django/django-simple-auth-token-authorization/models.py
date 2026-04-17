from django.conf import settings
from django.db import models
from django.utils import timezone

from .token import gen_token


class APIToken(models.Model):
    token = models.CharField("Token", max_length=64, primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField("Active", default=True)
    description = models.TextField("Description", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True, db_index=True)
    last_used = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = gen_token()
        # you might wanna deal with this in a better way
        # if expires_at is not set, default to 100 years from now
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(days=36500)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Token for {self.user.username}"
