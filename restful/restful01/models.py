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


############### Django contenttypes ##################
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Course(models.Model):
    """
    普通课程
    """
    title = models.CharField(max_length=32)
    # 仅用于反向查找
    price_policy_list = GenericRelation("PricePolicy")


class DegreeCourse(models.Model):
    """
    中级课程
    """
    title = models.CharField(max_length=32)

    # 仅用于反向查找
    price_policy_list = GenericRelation("PricePolicy")


class PricePolicy(models.Model):
    """
    价格策略
    """
    price = models.IntegerField()
    period = models.IntegerField()

    content_type = models.ForeignKey(ContentType, verbose_name='关联的表名称')
    object_id = models.IntegerField(verbose_name='关联的表中的数据行的ID')

    # 帮助你快速实现content_type操作
    content_object = GenericForeignKey('content_type', 'object_id')


