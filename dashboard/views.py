from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required(login_url="/accounts/login/")
def DashboardView(request):
    context = {}
    return render(request, "dashboard/dashboard.html", context=context)
