from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
import json

from .game.Game import Game

from .models import *

def index(request):
    context = {}
    return render(request, "opensauceapp/index.html", context)


def lobby(request, lobby_name):
    context = {}
    context["lobby_name"] = lobby_name
    context["lobby_name_json"] = json.dumps(lobby_name)
    context["report_categories"] = ReportCategory.objects.all()
    return render(request, "opensauceapp/lobby.html", context)


def lobbies_list(request):
    data = {"list": []}
    lobbies = Game.get_instance().get_lobbies_list()
    for lobby in lobbies.values():
        l = {
            "name": lobby.name,
            "total": lobby.count(),
            "players": lobby.count_players(),
            "spectators": lobby.count_spectators()
        }
        data["list"].append(l)

    return JsonResponse(data)


@never_cache
@login_required
def reports(request):
    context = {}
    return render(request, "opensauceapp/reports.html", context)

@csrf_exempt
def add(request):
    if request.method == "GET":
        context = {}
        context["sauce_categories"] = SauceCategory.objects.all()
        return render(request, "opensauceapp/add.html", context)
    elif request.method == "POST":
        data = json.loads(request.body)
        print(data)
        return JsonResponse({})
