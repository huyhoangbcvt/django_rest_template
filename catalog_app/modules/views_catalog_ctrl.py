from django.shortcuts import render, resolve_url, redirect
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class CatalogView(TemplateView, LoginRequiredMixin):
    # model = User
    # from pprint import pprint; pprint('author')
    context_object_name = 'catalog'
    template_name = 'home_catalog.html'
