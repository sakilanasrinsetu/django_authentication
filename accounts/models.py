from django.db.models import JSONField

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, User, UserManager
import uuid
from django.utils import timezone
from random import randint
from django.utils.timezone import timedelta

# Create your models here.



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        username = self.model.normalize_username(username)
        user = self.model(
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class UserAccount(AbstractUser):
    username = None
    last_name = None

    email = models.EmailField(max_length=35, unique=True)
    phone = models.CharField(max_length=35, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]
    objects = UserManager()