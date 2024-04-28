rom django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)  # Adding username field
    password = models.CharField(max_length=128)

    def _str_(self):
        return self.username
    
    pass


    # Define a custom intermediary model for the groups field
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='user_set_custom',
        related_query_name='user_custom',
        through='UserGroup',
    )

    # Define a custom intermediary model for the user_permissions field
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='user_set_custom',
        related_query_name='user_custom',
        through='UserPermission',
    )

# Custom intermediary model for the groups field
class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


# Custom intermediary model for the user_permissions field
class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
