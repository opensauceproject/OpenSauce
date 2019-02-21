<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy

from .models import BaseModel

# Create your views here.
def index(request):
    context = {}
    return render(request, 'opensauceapp/index.html', context)


'''
class DashboardView(generic.TemplateView):
    template_name = "resistanceapp/dashboard.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['categories'] = Category.objects.all()
        context['best_soldiers'] = Soldier.objects.order_by('-strength')[:3]
        context['nb_alive'] = Soldier.objects.filter(alive=True).count()
        context['nb_dead'] = Soldier.objects.filter(alive=False).count()

    # TODO-6-0 - Write queries for categories, 3 best soldiers by strength, count alive soldiers, count dead soldiers


    # TODO-3-0 Create the soldier list view with django class based views
class SoldierListView(generic.ListView):
    model = Soldier
    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['categories'] = Category.objects.all()
    #    context['best_soldiers'] = Soldier.objects.order_by('-strength')[:3]
    #    context['nb_alive'] = Soldier.objects.filter(alive=True).count()
    #    context['nb_dead'] = Soldier.objects.filter(alive=False).count()

    # TODO-3-2 Create the soldier detail view with django class based views
class SoldierDetailView(generic.DetailView):
    model = Soldier

class SoldierCreateView(generic.CreateView):
    model = Soldier
    fields = ['name', 'description', 'strength', 'age', 'alive',] #'category']
    success_url = reverse_lazy('dashboard-soldiers')

class SoldierUpdateView(generic.UpdateView):
    model = Soldier
    fields = ['name', 'description', 'strength', 'age', 'alive',]# 'category']
    success_url = reverse_lazy('dashboard-soldiers')

class SoldierDeleteView(generic.DeleteView):
    model = Soldier
    success_url = reverse_lazy('dashboard-soldiers')
'''
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> aa36622bbdb160f9e21396d24fbb66626ff08ef1
