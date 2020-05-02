from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from operations import (models, forms)


class OperationListView(ListView):
    model = models.Operation
    paginate_by = 100
