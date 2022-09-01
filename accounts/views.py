from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView


@login_required
def home(request):
    return render(request, 'registration/adminlte/base.html')

# Create your views here.
class HomeView(LoginRequiredMixin, ListView):
    pass
