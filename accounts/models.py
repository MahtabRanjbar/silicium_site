from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_author = models.BooleanField(default=False)
    special_user_time = models.DateTimeField(default=timezone.now)
    
    def is_special_user(self):
        if self.special_user_time > timezone.now():
            return True
        else:
            return False
        
