from django.urls import path
from django.contrib import admin
from django.views.generic.base import RedirectView

from . import views
from django.contrib.auth import views as reg_views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'lobby/<lobby_name>/', views.lobby, name='lobby'),
    path(r'lobby/', RedirectView.as_view(url='/')),
    path(r'lobbies_list/', views.lobbies_list, name='lobbies_list'),

    path(r'reports/', views.reports, name='reports'),
    path(r'report_add/', views.report_add, name='report_add'),
    path(r'report_ignore/', views.report_ignore, name='report_ignore'),
    path(r'report_delete/', views.report_delete, name='report_delete'),

    path(r'add/', views.add, name='add'),
    path(r'sauce_infos/<sauce_id>', views.sauce_infos, name='sauce_infos'),

    # Auth. System
    path(r'login/', reg_views.LoginView.as_view(), name='login'),
    path(r'logout/', reg_views.LogoutView.as_view(), name='logout'),
]
