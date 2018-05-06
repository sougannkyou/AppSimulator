from __future__ import absolute_import, unicode_literals

# django-celery
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.


# import pymysql
# pymysql.install_as_MySQLdb()
#
# from django.db.models.signals import post_syncdb
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth.models import Permission
#
#
# def add_view_permissions(sender, **kwargs):
#     """
#     This syncdb hooks takes care of adding a view permission too all our
#     content types.
#     """
#     # for each of our content types
#     for content_type in ContentType.objects.all():
#         # build our permission slug
#         codename = "view_%s" % content_type.model
#
#         # if it doesn't exist..
#         if not Permission.objects.filter(content_type=content_type, codename=codename):
#             # add it
#             # model_name = '%s\.%s'
#
#             Permission.objects.create(content_type=content_type,
#                                       codename=codename,
#                                       name="可以查看 %s" % content_type.name)
#
#
# # check for all our view permissions after a syncdb
# post_syncdb.connect(add_view_permissions)
#
# from django.db.backends.mysql.features import DatabaseFeatures
#
# DatabaseFeatures.allows_auto_pk_0 = True
