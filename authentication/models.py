from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CREATOR = 'CREATOR'
    SUBSCRIBER = 'SUBSCRIBER'

    ROLE_CHOICE = (
        (CREATOR, 'CREATOR'),
        (SUBSCRIBER, 'SUBSCRIBER'),
    )

    profile_photo = models.ImageField()
    role = models.CharField(max_length=30, choices=ROLE_CHOICE)

