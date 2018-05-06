# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_admin', '0002_objtype_userdeploy_userlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdeploy',
            name='wx_url',
            field=models.IntegerField(default=0, verbose_name='微信静态url转换次数'),
        ),
    ]
