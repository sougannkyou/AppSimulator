# coding=utf-8
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import Permission
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django import apps
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import logging
import os
import json

from .forms import *
from .models import User, PermissionGroups, UserConfigManagerLevel

# from config.models import Config

# Create your views here.

logget = logging.getLogger('backend_admin.views')
global_messages = {
    'success_add': '添加成功',
    'success_change': '修改成功',
    'error_select': '内容不存在',
    'no_valid': '数据有误',
    'no_perm': '您没有相关权限',

}


# 测试是否能链接界面
def test(request):
    return HttpResponse('ok12')


@login_required
def reload_uwsgi(request):
    '''
    重启uwsgi
    :param request:
    :return:
    '''
    if request.user.is_superuser is True:
        # os.system('uwsgi reload  /tmp/uwsgi.pid')
        os.system("kill -HUP `cat /tmp/uwsgi.pid`")
        messages.success(request, '重启uwsgi成功')
        return redirect(reverse('backend_admin:index'))


@login_required
def index(request):
    '''
    首页
    :param request:
    :return:
    '''
    return render(request, 'base_backend.html')


def login_view(request):
    '''
    登录
    :param request:
    :return:
    '''

    if request.method == 'GET':
        # 记住来源的url，如果没有则设置为首页('/')
        login_from = str(request.META.get('QUERY_STRING')).split('=')[-1]
        if login_from in ['', None, '/logout']:
            login_from = '/'
        request.session['login_from'] = login_from

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active == 0:
                messages.error(request, '请联系管理员开通您的账户')
                return redirect(reverse('backend_admin:login'))
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            request.session['user_id'] = user.id
            if 'login_from' not in request.session:
                request.session['login_from'] = '/'
            return redirect(request.session['login_from'])
        else:
            messages.error(request, '账户名或密码有误')
            return redirect(reverse('backend_admin:login'))

    return render(request, 'backend_admin/login.html', locals())


# 返回内容通用函数
@csrf_exempt
def visual_config_response(result):
    response = JsonResponse(result)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET'
    response['Access-Control-Allow-Credentials'] = 'true'
    response['Access-Control-Allow-Headers'] = 'k1, k2'
    response['Access-Control-Max-Age'] = 30  # 复杂请求时，“预检”缓存时间
    return response


# 可视化化配置登录
@csrf_exempt
def visual_login_view(request):
    '''
    可视化配置登录
    :param request:
    :return:
    '''
    if request.method == 'POST':
        conf_data = request.POST.get('conf_data')
        if conf_data:
            conf_args = json.loads(conf_data)
            username = conf_args['account']
            password = conf_args['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active == 0:
                    result = {'res': 0, 'mes': '用户无效'}
                    response = visual_config_response(result)
                    return response
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                request.session['user_id'] = user.id
                result = {'res': 1}
                response = visual_config_response(result)
            else:
                result = {'res': 0, 'mes': '用户名或密码错误'}
                response = visual_config_response(result)
            return response
        else:
            result = {'res': 0, 'mes': '接收参数错误'}
            response = visual_config_response(result)
            return response
    else:
        return HttpResponse('ok')


# 可视化配置登录验证
@csrf_exempt
def visual_login_verify(request):
    '''
    可视化配置cookie验证
    :param request:
    :return:
    '''
    if request.method == 'POST':
        conf_data = request.POST.get('conf_data')
        if conf_data:
            conf_args = json.loads(conf_data)
            cookie_post = conf_args['cookie']
            if cookie_post:
                if cookie_post == 'zhxg1234':
                    result = {'res': 1, 'username': 'lixuan', 'password': 'abcd1234'}
                    response = visual_config_response(result)
                    return response
                else:
                    result = {'res': 0, 'mes': 'cookie验证错误'}
                    response = visual_config_response(result)
                return response
        else:
            result = {'res': 0, 'mes': '接收参数错误'}
            response = visual_config_response(result)
            return response
    else:
        return HttpResponse('ok')


@login_required
def logout_view(request):
    '''
    退出
    :param request:
    :return:
    '''
    try:
        logout(request)
    except Exception as e:
        logget.error(e)
        messages.error(request, '您还没有登录，请登陆后再进行退出操作！')
        return redirect(reverse('backend_admin:login'))
    # messages.add_message(request, messages.INFO, message='成功退出')
    messages.info(request, '成功退出')
    return redirect(reverse('backend_admin:login'))


@login_required
def perm_deny(request):
    '''
    权限不足页面
    :param request:
    :return:
    '''
    return render(request, 'backend_admin/403.html', locals())


@login_required
def page_no(request):
    '''
    404页面
    :param request:
    :return:
    '''
    return render(request, 'backend_admin/404.html', locals())


@login_required
def private(request):
    '''
    个人中心，包括修改用户名，姓名，密码等
    :param request:
    :return:
    '''
    user = User.objects.get(pk=request.user.pk)
    username = user.username
    role = user.role
    group_config_each = user.userconfigeach_set.all()
    manager_groups = user.userconfigmanagerlevel_set.all()
    data = {'username': username, 'nickname': user.nickname, 'email_required': user.email_required, }
    form = PrivateForm(instance=user)

    if request.method == 'POST':
        form = PrivateForm(request.POST, instance=user)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, global_messages['success_change'])
                return redirect(reverse('backend_admin:private', ))
        else:
            messages.error(request, global_messages['no_valid'])
    return render(request, 'backend_admin/private.html', locals())


@login_required
def change_list(request, app_label, model_name):
    '''
    展示user,group等所有数据
    :param request:
    :param app_label:
    :param model_name:
    :return:
    '''
    allow_models = ('user', 'group', 'BConf')
    if model_name not in allow_models:
        messages.error(request, '您输入的链接有误')
        return redirect(reverse('backend_admin:index'))
    model_name = model_name
    app_label = app_label
    model = apps.apps.get_model(app_label, model_name=model_name)
    view_perm = '%s.view_%s' % (app_label, model_name)
    view_perm_verify = request.user.has_perm(view_perm)
    add_perm = '%s.add_%s' % (app_label, model_name)
    add_perm_verify = request.user.has_perm(add_perm)
    delete_perm = '%s.delete_%s' % (app_label, model_name)
    delete_perm_verify = request.user.has_perm(delete_perm)
    if view_perm_verify is False:
        messages.error(request, global_messages['no_perm'])
        return redirect(reverse('backend_admin:index'))

    try:
        model_verbose_name = model.Meta.verbose_name
    except Exception:
        model_verbose_name = model.__name__
    if model_verbose_name == 'Group':
        model_verbose_name = '分组'

    user_list_fields = ('username', 'email_required', 'nickname', 'role', 'is_active')
    field_name = User._meta.get_field('username')
    user_list_display_link = ('username',)
    group_list_fields = ('name', '人员')
    group_list_display_link = ('name',)

    list_fields_all = {'user': user_list_fields, 'group': group_list_fields, }
    list_display_links = {'user': user_list_display_link, 'group': group_list_display_link, }

    model_objects = model.objects.all()
    model_list_fields = list_fields_all[model_name]
    model_list_display_link = list_display_links[model_name][0]
    result_list = []
    for i in model_objects.values():
        obj_dict = dict()
        obj_list = []
        for j in model_list_fields:
            field_dict = dict()
            if app_label == 'auth' and model_name == 'group' and j == '人员':
                field_dict['value_all'] = model.objects.filter(id=i['id'])[0].user_set.all()
                field_dict['value'] = str(len(field_dict['value_all']))
            else:
                field_dict['value'] = i[j]
            if j == model_list_display_link:
                field_dict['is_link'] = True
                field_dict['link'] = '/backend_admin/%s/%s/%s/' % (app_label, model_name, i['id'])
                # 以下为暂时使用，等到功能菜单确定后删除
                # if app_label == 'config':
                #     field_dict['link'] = '/%s/%s/%s' % (app_label, model_name, i['id'])
            else:
                field_dict['is_link'] = False
            obj_list.append(field_dict)
        obj_dict['id'] = i['id']
        obj_dict['values'] = obj_list
        result_list.append(obj_dict)

    add_urls = '/backend_admin/%s/%s/add/' % (app_label, model_name)
    # if app_label == 'config':
    #     add_urls = '/%s/%s/add/' % (app_label, model_name)
    # return render(request, 'backend_admin/test.html', locals())
    return render(request, 'backend_admin/change_list.html', locals())


@login_required
def model_object_delete(request, app_label, model_name):
    '''
    删除user,group等内容
    :param request:
    :param app_label:
    :param model_name:
    :return:
    '''
    if request.method == 'POST':
        delete_perm = '%s.delete_%s' % (app_label, model_name)
        if request.user.has_perm(delete_perm) is False:
            messages.error(request, global_messages['no_perm'])
            return redirect(reverse('backend_admin:index'))
        objects_list = request.POST.getlist('td_checkbox')
        if len(objects_list) == 0:
            messages.warning(request, '请选择要删除的选项')
        else:
            model = apps.apps.get_model(app_label, model_name)
            for i in objects_list:
                model_obj = model.objects.filter(pk=i)
                if app_label == 'auth' and model_name == 'group':
                    group_users = model_obj[0].user_set.all()
                    list1 = list()
                    for j in group_users:
                        list1.append(j.id)
                    model_obj.delete()

                    for user_id in list1:
                        User.objects.get(id=int(user_id)).save()
                        # user.re_save()
                else:
                    model_obj.delete()
            messages.success(request, '删除成功')
    else:
        messages.error(request, '数据输入有误')
    return redirect(reverse('backend_admin:change_list', args=(app_label, model_name)))


@login_required
@permission_required('backend_admin.add_user', raise_exception=True)
def create_user(request):
    '''
    创建用户
    :param request:
    :return:
    '''
    form = CreateUserForm(initial={'is_active': 1})
    if request.META['HTTP_UPGRADE_INSECURE_REQUESTS'] == 1:
        pass
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            nickname = form.cleaned_data['nickname']
            email = form.cleaned_data['email_required']
            is_active = form.cleaned_data['is_active']
            groups_permissions = form.cleaned_data['groups_permissions']
            user_permissions_list = request.POST.getlist('checkbox_permission')
            user_create = User(username=username, email_required=email, nickname=nickname, is_active=is_active,
                               )
            user_create.set_password(password)
            user_create.save()
            try:
                send_mail('智慧星光采集管理后台账户', '欢迎注册智慧星光采集管理后台\n您的注册信息为：\n'
                                          '账户名：%s  密码：%s' % (username, password),
                          settings.EMAIL_HOST_USER, [email, ])
            except Exception as e:
                msg = '创建用户邮件错误：发送至用户%s邮箱%s出现错误，具体信息如下（%s）' % (username, email, e)
                logget.error(msg)

            for permission in user_permissions_list:
                user_permission = Permission.objects.get(name=permission)
                user_create.user_permissions.add(user_permission)
            for group_permission in groups_permissions:
                if group_permission.name == '管理员':
                    user_create.is_staff = 0
                user_create.groups.add(group_permission)
            user_create.save()
            messages.success(request, '添加成功')
            return redirect(reverse('backend_admin:create_user'))
        else:
            messages.error(request, '数据输入有误')
    return render(request, 'backend_admin/create_user.html', locals())


@permission_required('backend_admin.change_user', raise_exception=True)
def change_user(request, user_id):
    '''
    修改用户信息（管理员用）
    :param request:
    :param user_id: 用户id
    :return:
    '''
    change = 1
    try:
        user = User.objects.get(pk=user_id)
    except Exception:
        messages.error(request, '查询的用户不存在')
        return HttpResponse('error')
    username = user.username
    data = {'username': username, 'is_active': user.is_active, 'nickname': user.nickname,
            'email_required': user.email_required, 'groups_permissions': user.groups.all(),
            }
    form = ChangeUserForm(initial=data)

    if request.method == 'POST':
        form = ChangeUserForm(request.POST, initial=data)
        if form.is_valid():
            if form.has_changed():
                for i in form.changed_data:
                    if i == 'groups_permissions':
                        user.groups.clear()
                        user.is_staff = 0
                        groups_permissions = form.cleaned_data['groups_permissions']
                        for group_permission in groups_permissions:
                            if group_permission.name == '管理员':
                                user.is_staff = 1
                            user.groups.add(group_permission)
                    else:
                        setattr(user, i, form.cleaned_data[i])
                        user.i = form.cleaned_data[i]
                user_permissions_list = request.POST.getlist('checkbox_permission')
                for permission in user_permissions_list:
                    user_permission = Permission.objects.get(name=permission)
                    user.user_permissions.add(user_permission)
                user.nickname = form.cleaned_data['nickname']
                user.save()
                messages.success(request, global_messages['success_change'])
                return redirect(reverse('backend_admin:change_user', args=(user_id,)))
        else:
            messages.error(request, global_messages['no_valid'])
    return render(request, 'backend_admin/create_user.html', locals())


@login_required
def username_duplicate_verify(request):
    '''
    用户重复性验证
    :param request:
    :return:
    '''
    response = 0
    if request.method == 'POST':
        username_duplicate = request.POST.get('username_duplicate')
        username = request.POST.get('username')
        if len(User.objects.filter(username=str(username_duplicate))) > 0:
            if User.objects.filter(username=str(username_duplicate))[0].username != username:
                response = 1
            else:
                response = 2
    return HttpResponse(response)


@login_required
def email_duplicate_verify(request):
    '''
    用户邮箱重复性验证
    :param request:
    :return:
    '''
    response = 0
    if request.method == 'POST':
        email = request.POST.get('email_duplicate')
        username = request.POST.get('username')
        if len(User.objects.filter(email_required=str(email))) > 0:
            if User.objects.filter(email_required=str(email))[0].username != username:
                response = 1
            else:
                response = 2
    return HttpResponse(response)


@login_required
@permission_required('backend_admin.change_user', raise_exception=True)
def change_user_password(request, user_id):
    '''
    修改用户密码（管理员界面）
    :param request:
    :param user_id:
    :return:
    '''
    user = User.objects.get(pk=user_id)
    username = user.username
    email = user.email_required
    change_password_form = PasswordForm()
    if request.method == 'POST':
        change_password_form = PasswordForm(request.POST)
        if change_password_form.is_valid():
            password_new = change_password_form.cleaned_data['password1']
            user.set_password(password_new)
            user.save()
            try:
                send_mail('智慧星光采集管理后台账户修改', '管理员重置了您的密码\n您修改后的账户信息为：\n'
                                            '账户名：%s  密码：%s' % (username, password_new),
                          settings.EMAIL_HOST_USER, [email, ])
            except Exception as e:
                import traceback
                mes = traceback.format_exc()
                logget.error(mes)
                msg = '修改密码邮件错误：发送至用户%s邮箱%s出现错误，具体信息如下（%s）' % (username, email, e)
                logget.error(e)
            messages.success(request, '修改密码成功')
    return render(request, 'backend_admin/change_password.html', locals())


@login_required
@permission_required('backend_admin.change_user', raise_exception=True)
def change_password(request):
    '''
    修改密码（用户界面）
    :param request:
    :return:
    '''
    change_password_form = ChangePasswordForm()
    user_id = request.user.pk
    if request.method == 'POST':
        change_password_form = ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            username = request.user.username
            password_now = change_password_form.cleaned_data['now_password']
            password_new = change_password_form.cleaned_data['password1']
            user = authenticate(username=username, password=password_now)
            if user:
                user_object = User.objects.get(username=username)
                user_object.set_password(password_new)
                user_object.save()
                user_object1 = User.objects.get(username=username)
                messages.success(request, '修改密码成功，请重新登录！')
                return redirect(reverse('backend_admin:login'))
            else:
                messages.error(request, '您输入的密码有误，请重新输入')
    return render(request, 'backend_admin/change_password.html', locals())


@login_required
@permission_required('backend_admin.add_group', raise_exception=True)
def add_group(request):
    '''
    增加权限组
    :param request:
    :return:
    '''
    group_form = GroupForm()
    name = '权限'
    # 2-permission, 4-contenttype
    group_form.fields['permissions'].queryset = Permission.objects.exclude(content_type_id__in=[2, 4])
    if request.method == 'POST':
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            group1 = group_form.save(commit=True)
            messages.success(request, global_messages['success_add'])
    return render(request, 'backend_admin/creat_group.html', locals())


@login_required
@permission_required('backend_admin.change_group', raise_exception=True)
def change_group(request, group_id):
    '''
    修改权限组
    :param request:
    :param group_id:
    :return:
    '''
    group_id = group_id
    try:
        group = Group.objects.get(pk=group_id)
    except Exception:
        messages.error(request, global_messages['error_select'])
        return redirect(reverse('backend_admin:change_group', args=(group_id,)))
    group_form = GroupForm(instance=group)
    name = '权限'
    # 2-permission, 4-contenttype
    group_form.fields['permissions'].queryset = Permission.objects.exclude(content_type_id__in=['2', '4'])
    if request.method == 'POST':
        group_form = GroupForm(request.POST, instance=group)
        group_form.fields['permissions'].queryset = Permission.objects.exclude(content_type_id__in=['2', '4'])
        if group_form.is_valid():
            if group_form.has_changed():
                group_form.save()
                messages.success(request, global_messages['success_change'])
        else:
            messages.error(request, global_messages['error_select'])
            return redirect(reverse('backend_admin:change_group', args=(group_id,)))

    return render(request, 'backend_admin/creat_group.html', locals())


@login_required
def trans_users(request):
    if request.user.is_superuser:
        from config.models import BUser
        old_users = BUser.objects.all()
        password = 'abcd1234'
        num = 0
        for user in old_users:
            new_users_get = User.objects.filter(nickname=user.nickname)
            new_users_get2 = User.objects.filter(username=user.username)
            if new_users_get.count() == 0 and new_users_get2.count() == 0:
                user_create = User(id=user.id, username=user.username, nickname=user.nickname, is_active=True)
                user_create.set_password(password)
                user_create.save()
                num += 1
        mes = '修改成功，共修改了{}条数据！'.format(num)
        return HttpResponse(mes)
    else:
        return HttpResponse(status=403)