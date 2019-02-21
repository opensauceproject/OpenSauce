from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'lobby/<lobby_name>/', views.lobby, name='lobby'),
]
