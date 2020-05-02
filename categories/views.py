from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from categories import (models, forms)


class TypeListView(ListView):
    model = models.Type


class CategoryListView(ListView):
    model = models.Category


class MerchantCodeListView(ListView):
    model = models.MerchantCode


class DescriptionListView(ListView):
    model = models.Description

