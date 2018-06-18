# coding=utf-8
from pprint import pprint
import datetime
import json
from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from .dbDriver import MongoDriver
from django.core.urlresolvers import reverse

MDB = MongoDriver()

# [数据面板]
class DashBoardView(TemplateView):
    queryset = []
    template_name = 'AppSimulator/dashboard.html'

# [数据面板]
class TasksView(TemplateView):
    queryset = []
    template_name = 'AppSimulator/tasks.html'