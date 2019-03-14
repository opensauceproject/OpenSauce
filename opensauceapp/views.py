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


# used to fetch the info when reporting
def sauce_infos(request, sauce_id):
    data = {}
    sauce = Sauce.objects.select_related("sauce_category").filter(id=sauce_id)[0]
    data["question"] = sauce.question
    data["answer"] = sauce.answer
    data["media_type"] = sauce.media_type
    data["sauce_category"] = sauce.sauce_category.name
    return JsonResponse(data)

@never_cache
@login_required
def reports(request):
    context = {}
    return render(request, "opensauceapp/reports.html", context)

# no need of the csrf because anybody can use this route
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

# no need of the csrf because anybody can use this route
@csrf_exempt
def report_add(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # 'report_categories_ids': ['1', '2'], 'text': 'asdsad', 'sauce_id': 3
        report = Report()
        sauces = Sauce.objects.filter(id=data["sauce_id"])
        if len(sauces) <= 0:
            return HttpResponseBadRequest()
        report.sauce = sauces[0]
        report.additional_informations = data["additional_informations"]
        report.save()

        for category_id in data["report_categories_ids"]:
            report_report_category = ReportReportCategory()
            report_report_category.report = report
            report_categories = ReportCategory.objects.filter(id=category_id)
            if len(report_categories) <= 0:
                return HttpResponseBadRequest()
            report_report_category.report_category = report_categories[0]
            report_report_category.save()

        print(data)
    return JsonResponse({})
