from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)  # Adding username field
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class FailedLoginAttempt(models.Model):
    username = models.CharField(max_length=150)
    attempts = models.PositiveIntegerField(default=0)
    last_attempt = models.DateTimeField(null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Failed login attempts"

# Custom intermediary model for the groups field
class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

# Custom intermediary model for the user_permissions field
class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
