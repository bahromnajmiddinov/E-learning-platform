from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name'
    )
    
    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        return f'{self.first_name} | {self.email}'
    
    @property
    def get_avatar_url(self):
        return self.avatar.url if self.avatar else None


class Balance(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=1000)
    
    class Meta:
        ordering = ['-id']
    