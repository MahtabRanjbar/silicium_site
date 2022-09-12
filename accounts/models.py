import os
from pathlib import Path

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.


def upload_file_name(instance, filename):
    """Return the location to upload the file."""

    _, file_extension = os.path.splitext(filename)
    return Path('users/', instance.username, 'profile_picture.png')


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to=upload_file_name, null=True, blank=True)
    is_author = models.BooleanField(default=False)
    special_user_time = models.DateTimeField(default=timezone.now)
    
    def is_special_user(self):
        if self.special_user_time > timezone.now():
            return True
        else:
            return False
    is_special_user.boolean = True
        
