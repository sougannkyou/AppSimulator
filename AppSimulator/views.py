# coding=utf-8
from django.views.generic import TemplateView

# [数据面板]
class DashBoardView(TemplateView):
    queryset = []
    template_name = 'AppSimulator/dashboard.html'


# [数据面板]
class TasksView(TemplateView):
    queryset = []
    template_name = 'AppSimulator/tasks.html'
