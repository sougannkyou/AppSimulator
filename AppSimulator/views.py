# coding=utf-8
from django.views.generic import TemplateView
from AppSimulator.DBLib import MongoDriver

MDB = MongoDriver()

# [数据面板]
class DashBoardView(TemplateView):
    queryset = []
    template_name = 'AppSimulator/dashboard.html'

# [数据面板]
class TasksView(TemplateView):
    queryset = []
    template_name = 'AppSimulator/tasks.html'