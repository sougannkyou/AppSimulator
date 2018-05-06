# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_admin', '0007_auto_20170607_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='departments',
            name='level',
            field=models.IntegerField(verbose_name='部门级别', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='departments',
            name='parent',
            field=models.IntegerField(default=0, verbose_name='所属部门'),
        ),
    ]
