from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from .manager import UserManager


TASK_CHOICES =(
    ("active_account", "Active Account"),
    ("reset_pass", "Reset Password"),
)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique = True)
    otp = models.CharField(max_length = 6, null=True, blank=True)
    has_used = models.BooleanField(default=False)
    task_type = models.CharField(max_length = 100, choices = TASK_CHOICES)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name
    
    def __str__(self):
        return self.email