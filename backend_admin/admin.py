from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth import models as auth_models

from backend_admin.models import *

# admin.site.site_header = '智慧星光采集后台'
# admin.site.site_title = '项目管理'


# Register your models here.
admin.site.register(UserConfigEach)
admin.site.register(UserConfigManagerLevel)
admin.site.register(GroupConfigEach)
admin.site.register(GroupConfigManager)
admin.site.register(Departments)


class PermissionAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(auth_models.Permission, PermissionAdmin)


class PermissionGroupsAdmin(admin.ModelAdmin):
    filter_horizontal = ['groups_permissions']


admin.site.register(PermissionGroups, PermissionGroupsAdmin)


# useradmin
class StarUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('nickname', 'email_required')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        (_('Personal info'), {'fields': ('nickname', 'email_required')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions', )}),
    )

    list_display = ('username', 'email_required', 'nickname', 'role', 'is_active')
    search_fields = ('username', 'email_required', 'nickname', 'role')
admin.site.register(User, StarUserAdmin)
