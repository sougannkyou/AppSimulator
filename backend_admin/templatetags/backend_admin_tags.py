# coding:utf-8
from django import template

from backend_admin.models import *

register = template.Library()


@register.simple_tag(name='permission_groups_filter')
def permission_groups_filter(groups_name):
    # print(groups_name)
    permissions_children = PermissionGroups.objects.get(groups_name='全站爬虫').groups_permissions.all()
    print(permissions_children)
    return permissions_children
