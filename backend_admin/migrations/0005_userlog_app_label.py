# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_admin', '0004_userlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='userlog',
            name='app_label',
            field=models.CharField(null=True, max_length=100, verbose_name='app名称'),
        ),
    ]
