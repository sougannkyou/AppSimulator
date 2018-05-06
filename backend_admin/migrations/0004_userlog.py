# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('backend_admin', '0003_auto_20170524_0958'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('author', models.CharField(verbose_name='用户姓名', max_length=100)),
                ('obj_type', models.CharField(verbose_name='对象类型', null=True, max_length=100)),
                ('obj', models.CharField(verbose_name='操作对象', null=True, max_length=100)),
                ('operate_type', models.CharField(verbose_name='操作类型', null=True, max_length=100)),
                ('operate', models.CharField(verbose_name='操作', null=True, max_length=100)),
                ('comment', models.CharField(verbose_name='备注', null=True, max_length=300)),
                ('time', models.IntegerField(verbose_name='操作时间', null=True)),
                ('user', models.ForeignKey(verbose_name='用户', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户操作记录',
                'verbose_name_plural': '用户操作记录',
                'ordering': ['-id'],
            },
        ),
    ]
