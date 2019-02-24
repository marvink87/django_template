from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user_obj = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user_obj

    def create_superuser(self, email, password=None):
        user_obj = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user_obj


class CustomUser(AbstractUser):
    # add additional fields in here
    email = models.EmailField(max_length=255, unique=True, blank=False, verbose_name='Email address')
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def username(self):
        return self.email

    @property
    def is_superuser(self):
        return self.admin

    @property
    def is_staff(self):
        return self.admin or self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def full_name(self):
        return self.get_full_name()
