# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import django.utils.timezone
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', error_messages={'unique': 'A user with that username already exists.'}, unique=True, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], verbose_name='username')),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, blank=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nickname', models.CharField(max_length=50, verbose_name='姓名')),
                ('email_required', models.EmailField(max_length=254, verbose_name='电子邮箱')),
                ('role', models.CharField(max_length=200, default='无角色', blank=True, verbose_name='角色')),
                ('groups', models.ManyToManyField(blank=True, related_query_name='user', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_query_name='user', help_text='Specific permissions for this user.', related_name='user_set', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': '用户',
                'ordering': ['-id'],
                'verbose_name': '用户',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AllSite',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('model_name', models.CharField(max_length=20, verbose_name='模块名称')),
            ],
            options={
                'verbose_name_plural': '全站爬虫',
                'ordering': ['-id'],
                'verbose_name': '全站爬虫',
            },
        ),
        migrations.CreateModel(
            name='GroupConfigEach',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='组名')),
                ('user', models.ForeignKey(verbose_name='创建者', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '配置分组',
                'ordering': ['-id'],
                'verbose_name': '配置分组',
            },
        ),
        migrations.CreateModel(
            name='GroupConfigManager',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='组名')),
                ('user', models.ForeignKey(verbose_name='创建者', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '配置管理组',
                'ordering': ['-id'],
                'verbose_name': '配置管理组',
            },
        ),
        migrations.CreateModel(
            name='PermissionGroups',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('groups_name', models.CharField(max_length=50, verbose_name='名称')),
                ('groups_permissions', models.ManyToManyField(to='auth.Permission', blank=True, verbose_name='权限')),
            ],
        ),
        migrations.CreateModel(
            name='UserConfigEach',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('level', models.IntegerField(default=0, blank=True)),
                ('group_config_each', models.ForeignKey(to='backend_admin.GroupConfigEach')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserConfigManagerLevel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('level', models.IntegerField(default=0, blank=True)),
                ('group_config_manager', models.ForeignKey(to='backend_admin.GroupConfigManager')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
