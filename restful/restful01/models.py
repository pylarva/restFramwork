from django.db import models

# Create your models here.


class UsersInfo(models.Model):
    """
    用户表
    """
    user_type_choice = (
        (1, 'normal'),
        (2, 'vip'),
        (3, 'svip')
    )
    user_type = models.IntegerField(choices=user_type_choice)
    username = models.CharField(max_length=32, unique=True)
    pwd = models.CharField(max_length=32)


class UsersToken(models.Model):
    """
    用户token表
    """
    user = models.OneToOneField(to='UsersInfo')
    token = models.CharField(max_length=64)

