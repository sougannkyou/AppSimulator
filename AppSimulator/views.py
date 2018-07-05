# coding=utf-8
from django.views.generic import TemplateView


class DashBoardView(TemplateView):
    queryset = []
    template_name = 'AppSimulator/dashboard.html'


class TasksView(TemplateView):
    queryset = []
    template_name = 'AppSimulator/tasks.html'


class VMConfView(TemplateView):
    queryset = []
    template_name = 'AppSimulator/vm_conf.html'
