from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", ]
    
    # Overriding the default related_name for groups and user_permissions fields
    groups = models.ManyToManyField(
        Group,
        related_name='userauth_user_set',  # Custom related name for reverse relation
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='userauth_user_permissions_set',  # Custom related name for reverse relation
        blank=True
    )
    
    def __str__(self):
        return self.username

    