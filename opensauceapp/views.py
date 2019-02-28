from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
import json

from .models import Sauce, Category

def index(request):
    context = {}
    return render(request, 'opensauceapp/index.html', context)

def lobby(request, lobby_name):
    return render(request, 'opensauceapp/lobby.html', {'lobby_name': lobby_name, 'lobby_name_json' : json.dumps(lobby_name)})

@login_required
def reports(request):
    context = {}
    return render(request, 'opensauceapp/reports.html', context)
