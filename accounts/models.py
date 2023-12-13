from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" 
    

class OneTimePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()

    
    def __str__(self):
        return f"{self.user.first_name}- passcode"



