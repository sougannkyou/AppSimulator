from django.conf.urls import url, patterns
from . import views
from django.views.generic import RedirectView

# from django.views.generic.simple import redirect_to
# from django.views.generic.simple import redirect_to

urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^changepassword$', views.change_password, name='change_password'),
    url(r'^private$', views.private, name='private'),
    url(r'^backend_admin/backend_admin/user/add/$', views.create_user, name='create_user', ),
    url(r'^backend_admin/backend_admin/user/(\d+)/password$', views.change_user_password, name='change_user_password', ),
    url(r'^backend_admin/backend_admin/user/(\d+)/$', views.change_user, name='change_user', ),
    url(r'^backend_admin/auth/group/add/$', views.add_group, name='add_group', ),
    url(r'^backend_admin/auth/group/(\d+)/$', views.change_group, name='change_group', ),
    # url(r'^admin/backend_admin/user/\d/$', RedirectView.as_view(url='/changeuser'),),
    # url(r'^admin/auth/group/$', RedirectView.as_view(url='/backend_admin/auth/group', permanent=True), ),

    url(r'^duplicate_username$', views.username_duplicate_verify, name='duplicate_username'),
    url(r'^duplicate_email$', views.email_duplicate_verify, name='duplicate_email'),
    url(r'^backend_admin/(\w+)/(\w+)/$', views.change_list, name='change_list'),
    url(r'^backend_admin/(\w+)/(\w+)/delete$', views.model_object_delete, name='model_object_delete'),

    url(r'^uwsgireload/$', views.reload_uwsgi, name='reload_uwsgi'),

    url(r'^visual/login$', views.visual_login_view, name='visual_login_view'),
    url(r'^visual/verify/$', views.visual_login_verify, name='visual_login_verify'),
    url(r'^trans_users/$', views.trans_users, name='trans_users'),
]
