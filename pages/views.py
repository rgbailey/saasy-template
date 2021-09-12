from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "pages/home.html"


class AboutView(TemplateView):
    template_name = "pages/about.html"


class ProductView(TemplateView):
    template_name = "pages/product.html"


class ContactView(TemplateView):
    template_name = "pages/contact.html"
