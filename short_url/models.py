from django.db import models
from uuid import uuid4
from django.utils.timezone import now
from datetime import timedelta


class UrlShortened(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    url = models.URLField(max_length=255, null=True)
    _name = models.CharField(max_length=255, null=True,
                             unique=True, name='name')
    date_expiration = models.DateTimeField(default=now() + timedelta(7))
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            self._name = str(uuid4())[:5]
        else:
            self._name = value

    def __str__(self):
        return self.url
