from django.urls import path
from django.contrib import admin
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'lobby/<lobby_name>/', views.lobby, name='lobby'),
    path(r'lobby/', RedirectView.as_view(url='/'), name='lobbyEmpty'),
    path(r'lobbiesList/', views.lobbyList, name='lobbiesList'),
]
