from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(blank=True)
    last_name = models.CharField(blank=True)
    email = models.EmailField(blank=True)


    def __str__(self):
        return self.username
