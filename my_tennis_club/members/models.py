from django.contrib.auth.models import AbstractUser
from django.db import models


class Member(AbstractUser):
    phone = models.IntegerField(null=True)
    joined_date = models.DateField(auto_now_add=True)
