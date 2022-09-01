from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'registration/home.html')

# Create your views here.
class HomeView(LoginRequiredMixin, ListView):
    pass
