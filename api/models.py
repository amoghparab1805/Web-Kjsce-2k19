from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
from .choices import GENDER_CHOICES

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, null=True)
    provider_id = models.CharField(max_length=50)
    photo_url =  models.CharField(max_length=1024, null=True)
    email = models.EmailField(null=True)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    age = models.CharField(max_length=5, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDER_CHOICES)

    def __str__(self):
        return self.username