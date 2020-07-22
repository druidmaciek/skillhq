from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="users/profile/%Y/%m/%d/", blank=True)
    cover = models.ImageField(upload_to="users/covers/%Y/%m/%d/", blank=True)
    about = models.TextField(max_length=450, blank=True)

    def __str__(self):
        return f"Profile for user {self.user.username}"
