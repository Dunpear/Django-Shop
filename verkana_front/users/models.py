from django.db import models


class User(models.Model):
    username = models.CharField(max_length=11)
    token = models.CharField(max_length=400)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.username

