from django.shortcuts import render
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"


# Create your views here.
