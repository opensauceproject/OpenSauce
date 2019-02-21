from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy

from .models import BaseModel

# Create your views here.
def index(request):
    context = {}
    return render(request, 'opensauceapp/index.html', context)
