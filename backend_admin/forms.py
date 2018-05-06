import re

from django import forms
from django.contrib.auth.models import Group

from backend_admin.models import User, PermissionGroups, GroupConfigEach, GroupConfigManager

from collections import OrderedDict


# 验证密码是否由数字和字母构成
def password_verify(val):
    if not re.search('\d', val) or not re.search('[a-zA-Z]', val):
        raise forms.ValidationError('密码缺少字母或数字！')


class ChangePasswordForm(forms.Form):
    now_password = forms.CharField(label='当前密码', max_length=16, min_length=6, required=True,
                                   widget=forms.PasswordInput(attrs={"size": '30', "class": 'required'}),
                                   validators=[password_verify, ],)
    password1 = forms.CharField(label='新密码', max_length=16, min_length=6, required=True,
                                widget=forms.PasswordInput(attrs={"size": '30', "class": 'required'}),
                                help_text='密码在6到16位之间，必须包含字母和数字')
    password2 = forms.CharField(label='请再次输入新密码', max_length=16, min_length=6, required=True,
                                widget=forms.PasswordInput(attrs={"size": '30', "class": 'required'}))

    def clean(self):
        if self.is_valid():
            password_1 = self.cleaned_data['password1']
            password_2 = self.cleaned_data['password2']
            if password_1 and password_2 and password_2 != password_1:
                raise forms.ValidationError('您输入的密码不一致')


class PasswordForm(forms.Form):
    password1 = forms.CharField(label='新密码', max_length=16, min_length=6,
                                widget=forms.PasswordInput(attrs={"size": '30', 'class': 'required'}),
                                help_text='密码在6到16位之间，必须包含字母和数字', required=True)
    password2 = forms.CharField(label='请再次输入新密码', max_length=16, min_length=6,
                                widget=forms.PasswordInput(attrs={"size": '30', 'class': 'required'}),
                                required=True)

    def clean(self):
        password_2 = self.cleaned_data['password2']
        password_1 = self.cleaned_data['password1']
        if password_1 and password_2 and password_2 != password_1:
            raise forms.ValidationError('您输入的密码不一致')


class BaseBackendUserForm(forms.ModelForm):
    is_active = forms.BooleanField(label='有效', required=False,
                                   help_text='用户是否可以登录此站点（是否离职）', )
    groups_permissions = forms.ModelMultipleChoiceField(label='组权限', queryset=Group.objects.all().order_by('pk'),
                                                        required=False,
                                                        widget=forms.CheckboxSelectMultiple,
                                                        )

    permissions = forms.ModelMultipleChoiceField(label='权限选择', queryset=PermissionGroups.objects.all(), required=False,
                                                 widget=forms.CheckboxSelectMultiple,
                                                 )
    group_config_each = forms.ModelMultipleChoiceField(label='配置组', queryset=GroupConfigEach.objects.all(),
                                                       required=False,
                                                       widget=forms.CheckboxSelectMultiple,
                                                       )
    group_config_manager = forms.ModelMultipleChoiceField(label='配置管理组', queryset=GroupConfigManager.objects.all(),
                                                          required=False,
                                                          widget=forms.CheckboxSelectMultiple,
                                                          )

    class Meta:
        model = User
        fields = ['username', 'nickname', 'email_required', ]
        widgets = {
            'username': forms.TextInput(attrs={"size": '30', 'class': 'required'}, ),
            'nickname': forms.TextInput(attrs={"size": '30', 'class': 'required'}),
            'email_required': forms.EmailInput(attrs={"size": '30', 'class': 'required', 'type': 'text'}, ),
        }
        help_texts = {
            'username': '不多于30个字符。只能用字母、数字和字符 @/./+/-/_ 。',
            'nickname': '请输入您的真实姓名。',
        }


class CreateUserForm(PasswordForm, BaseBackendUserForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        original_fields = self.fields
        new_order = OrderedDict()
        for key in ['username', 'password1', 'password2', 'nickname', 'email_required', 'is_active',
                    'groups_permissions', 'permissions', ]:
            new_order[key] = original_fields[key]
        self.fields = new_order

    def clean(self):
        password_2 = self.cleaned_data['password2']
        password_1 = self.cleaned_data['password1']
        email_required = self.cleaned_data['email_required']
        if password_1 and password_2 and password_2 != password_1:
            raise forms.ValidationError('您输入的密码不一致')
        if len(User.objects.filter(email_required=str(email_required))) > 0:
            raise forms.ValidationError('您注册的邮箱已经存在')


class ChangeUserForm(BaseBackendUserForm):
    def __init__(self, *args, **kwargs):
        super(ChangeUserForm, self).__init__(*args, **kwargs)
        original_fields = self.fields
        new_order = OrderedDict()
        for key in ['nickname', 'email_required', 'is_active', 'groups_permissions', 'permissions',
                    ]:
            new_order[key] = original_fields[key]
        self.fields = new_order


class PrivateForm(BaseBackendUserForm):
    def __init__(self, *args, **kwargs):
        super(PrivateForm, self).__init__(*args, **kwargs)
        original_fields = self.fields
        new_order = OrderedDict()
        for key in ['nickname', 'email_required', ]:
            new_order[key] = original_fields[key]
        self.fields = new_order


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions', ]
        widgets = {
            'name': forms.TextInput(attrs={"size": '30', 'class': 'required'}, ),
            'permissions': forms.SelectMultiple(attrs={"multiple": "multiple", "size": "10"}, ),
        }
