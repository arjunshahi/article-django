from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "custom_user"

