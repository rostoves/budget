from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'index.html'


class BalanceCheck(TemplateView):
    template_name = 'dashboard/balance_check.html'
