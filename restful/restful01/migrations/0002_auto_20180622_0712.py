# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-06-22 07:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restful01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='usersinfo',
            name='user_type',
            field=models.IntegerField(choices=[(1, '普通用户'), (2, 'vip'), (3, 'svip')]),
        ),
        migrations.AddField(
            model_name='usersinfo',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='restful01.Group'),
        ),
    ]
