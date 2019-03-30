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
import re
from PIL import Image
from io import BytesIO
import base64

from .game.Game import Game, Lobby
from .tools import get_client_ip

from .models import *
from .apps import DEBUG

def index(request):
    context = {}
    return render(request, "opensauceapp/index.html", context)


def lobby(request, lobby_name):
    lobby = Game.get_instance().get_lobby(lobby_name)
    if lobby_name not in request.session:
        if lobby.settings["password"] != "":
            return redirect("lobby_password", lobby_name=lobby_name)
    else:
        del request.session[lobby_name]
    context = {}
    context["lobby_name"] = lobby_name

    if DEBUG:
        protocol_websocket = "ws://"
    else:
        protocol_websocket = "wss://"

    context["lobby_socket_url"] = protocol_websocket + \
        request.get_host() + "/lobby/" + lobby_name + "/"
    context["lobby_name_json"] = json.dumps(lobby_name)
    context["report_categories"] = ReportCategory.objects.all()
    context["sauce_categories"] = SauceCategory.objects.all()
    context["score_goals"] = Lobby.score_goals
    context["default_score_goal"] = Lobby.default_score_goal
    return render(request, "opensauceapp/lobby/lobby.html", context)


def lobby_password(request, lobby_name):
    if request.method == "GET":
        if not Game.get_instance().lobby_exist(lobby_name):
            return redirect("/")
        lobby = Game.get_instance().get_lobby(lobby_name)
        if lobby.settings["password"] == "":
            return redirect("lobby", lobby_name=lobby_name)
        context = {}
        context["lobby_name"] = lobby.name
        context["url_lobby"] = "/lobby/" + \
            lobby.name  # find a way to get the name
        return render(request, "opensauceapp/lobby/password.html", context)
    elif request.method == "POST":
        data = {
            "lobby_exist": False,
            "need_password": False,
            "password_ok": False,
        }
        if Game.get_instance().lobby_exist(lobby_name):
            data["lobby_exist"] = True
            lobby = Game.get_instance().get_lobby(lobby_name)
            if lobby.settings["password"] != "":
                data["need_password"] = True
                if lobby.settings["password"] == request.POST["password"]:
                    data["password_ok"] = True
                    request.session[lobby_name] = True

        return JsonResponse(data)


def lobbies_list(request):
    data = {"list": []}
    lobbies = Game.get_instance().get_lobbies_list()
    for lobbyname, lobby in lobbies.items():

        print(lobbyname, lobby)
        total_count = lobby.count()
        # if total_count > 0:
        l = {
            "name": lobby.name,
            "total": total_count,
            "players": lobby.count_players(),
            "spectators": lobby.count_spectators(),
            "password": lobby.settings["password"] != ""
        }
        data["list"].append(l)
        # else:
            # Game.get_instance().remove_lobby(lobby.name)

    data["list"] = sorted(
        data["list"], key=lambda d: (-d["total"], -d["players"], -d["spectators"]))

    return JsonResponse(data)


# used to fetch the info when reporting
def sauce_infos(request, sauce_id):
    data = {}
    sauce = Sauce.objects.select_related(
        "sauce_category").filter(id=sauce_id)[0]
    data["question"] = sauce.question
    data["answer"] = sauce.answer
    data["media_type"] = sauce.media_type
    data["sauce_category"] = sauce.sauce_category.name
    return JsonResponse(data)


@never_cache
@login_required
def reports(request):
    context = {}
    context["sauce_reports"] = Report.objects.all()
    context["QUOTE"] = 0
    context["IMAGE"] = 1
    return render(request, "opensauceapp/reports.html", context)


# no need of the csrf because anybody can use this route
MAX_WIDTH = 1280
MAX_HEIGHT = 1024
MAX_RATIO = MAX_WIDTH / MAX_HEIGHT


@csrf_exempt
def add(request):
    if request.method == "GET":
        context = {}
        context["sauce_categories"] = SauceCategory.objects.all()
        return render(request, "opensauceapp/add.html", context)
    elif request.method == "POST":
        data = json.loads(request.body)
        sauce = Sauce()
        invalid = False
        sauce.answer = data["answer"]
        sauce.sauce_category = SauceCategory.objects.get(
            id=data["sauce_category"])
        sauce.difficulty = data["difficulty"]
        sauce.media_type = data["type"]
        if sauce.media_type == 0:
            # quote
            sauce.question = data["question"]
        elif sauce.media_type == 1:
            # image
            try:
                image64_split = re.match(
                    '(data:image/.+;base64,)(.*)', data["question"])
                image64_header = image64_split.group(1)
                image64_data = image64_split.group(2)

                image_data = base64.b64decode(image64_data)
                image = Image.open(BytesIO(image_data))
                width, height = image.size
                ratio = width / height

                # keep the min size
                resize_width = min(MAX_WIDTH, width)
                resize_height = min(MAX_HEIGHT, height)

                # correct the ratio
                # wider
                if ratio > MAX_RATIO:
                    resize_height = int(resize_width / ratio)
                # heigher
                else:
                    resize_width = int(resize_height * ratio)

                image = image.resize((resize_width, resize_height))

                buffered = BytesIO()
                image.save(buffered, format="PNG")
                binary_image64 = base64.b64encode(buffered.getvalue())

                img_str = image64_header + binary_image64.decode('utf-8')
                sauce.question = img_str
            except:
                invalid = True

        sauce.ip = get_client_ip(request)
        if not invalid:
            sauce.save()
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
        report.ip = get_client_ip(request)
        report.save()

        for category_id in data["report_categories_ids"]:
            report_report_category = ReportReportCategory()
            report_report_category.report = report
            report_categories = ReportCategory.objects.filter(id=category_id)
            if len(report_categories) <= 0:
                return HttpResponseBadRequest()
            report_report_category.report_category = report_categories[0]
            report_report_category.save()
    return JsonResponse({})


@login_required
@csrf_exempt
def report_ignore(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        report = Report.objects.get(id=data["id"])
        report.delete()
    return JsonResponse({})


@login_required
@csrf_exempt
def report_delete(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        data = json.loads(request.body)
        report = Report.objects.get(id=data["id"])
        report.sauce.delete()
        report.delete()
    return JsonResponse({})
