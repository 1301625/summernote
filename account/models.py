from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager ,PermissionsMixin

# Create your models here.
class user(AbstractBaseUser):
    email = models.EmailField(
        verbose_name= 'Email',
        max_length=255,
        unique= True,
    )
    nickname = models.CharField(
        '닉네임',
        max_length=10,
        blank=True,
        unique=True
    )
    name = models.CharField(
        '이름',
        max_length=10,

    )
