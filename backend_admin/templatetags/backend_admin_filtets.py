# coding:utf-8
from django import template
from django.contrib.auth.models import Group
from django.template.defaultfilters import stringfilter

from backend_admin.models import *

register = template.Library()


@register.filter(name='permission_groups_filter')
@stringfilter
def permission_groups_filter(groups_name):
    permissions_children = PermissionGroups.objects.get(groups_name=str(groups_name).strip()).groups_permissions.all()
    return permissions_children


@register.filter(name='groups_filter')
@stringfilter
def groups_filter(groups_name):
    groups_children = Group.objects.get(name=str(groups_name).strip()).permissions.all()
    return groups_children


@register.filter(name='has_group')
def has_group(user, group_name):
    if user.is_superuser == 1:
        return True
    try:
        group = Group.objects.filter(name=group_name)[0]
    except Exception:
        return False
    if group in user.groups.all():
        return True
    else:
        return False


@register.filter(name='user_filter')
@stringfilter
def user_filter(username):
    user = User.objects.get(username=str(username).strip())
    return user


@register.filter(name='object_filter')
@stringfilter
def object_filter(obj, field):
    print(obj)
    print(type(obj))
    print(field)
    # object_result = obj._meta.get_field_by_name(field)
    object_result = 1

    return object_result
