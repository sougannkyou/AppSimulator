# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_admin', '0006_departments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departments',
            name='member_num',
            field=models.IntegerField(verbose_name='部门人数', default=0),
        ),
    ]
