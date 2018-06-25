from django.db import models

# Create your models here.


class UsersInfo(models.Model):
    """
    用户表
    """
    user_type_choice = (
        (1, '普通用户'),
        (2, 'vip'),
        (3, 'svip')
    )
    user_type = models.IntegerField(choices=user_type_choice)
    username = models.CharField(max_length=32, unique=True)
    pwd = models.CharField(max_length=32)
    group = models.ForeignKey(to="Group", default=1)
    role = models.ManyToManyField(to="Roles", default=1)


class UsersToken(models.Model):
    """
    用户token表
    """
    user = models.OneToOneField(to='UsersInfo')
    token = models.CharField(max_length=64)


class Group(models.Model):
    """
    用户组表
    """
    title = models.CharField(max_length=32, unique=True)


class Roles(models.Model):
    """
    角色表
    """
    title = models.CharField(max_length=32, null=True)

