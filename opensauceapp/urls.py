from django.urls import path
from django.contrib import admin
from django.views.generic.base import RedirectView

from . import views
from django.contrib.auth import views as reg_views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'lobby/<lobby_name>/', views.lobby, name='lobby'),
    path(r'lobby/', RedirectView.as_view(url='/'), name='lobby'),
    path(r'reports/', views.reports, name='reports'),

    # Auth. System
    path('login/', reg_views.LoginView.as_view(), name='login'),
    path('logout/', reg_views.LogoutView.as_view(), name='logout'),
]
