import logging
from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.core.paginator import Paginator
from operations import (models as o_models, forms)
from categories import models as c_models

logger = logging.getLogger('django')


class OperationListView(ListView):
    model = o_models.Operation
    paginate_by = 100

    def get_queryset(self):
        filter_args = {}
        filter_args['status__in'] = [self.request.GET.get('status[]', 'OK')]
        if self.request.GET.get('merchant_code[]'):
            filter_args['merchant_code__in'] = [self.request.GET.get('merchant_code[]')]

        order = self.request.GET.get('orderby', 'date')

        new_context = o_models.Operation.objects.filter(
            **filter_args
        ).order_by(order)

        return new_context

    def get_context_data(self, **kwargs):
        context = super(OperationListView, self).get_context_data(**kwargs)
        context['status'] = get_column('Operation', 'status')
        context['merchant_code'] = get_row_and_id('MerchantCode', 'name')
        context['orderby'] = self.request.GET.get('orderby', 'date')
        return context


class OperationsView(OperationListView):
    template_name = 'operations/operations.html'

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('filter_applied'):
            operation_list = self.get_queryset()
            paginator = Paginator(operation_list, 100)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            print(page_obj)
            return render(request, 'operations/operation_list.html', {'operation_list': operation_list,
                                                                      'page_obj': page_obj})
        return super().get(request, *args, **kwargs)


def get_column(model, column):
    logger.info('Requested ' + column + ' from ' + model)
    objects = None
    array = []
    if model == 'Operation':
        objects = o_models.Operation.objects
    if model == 'MerchantCode':
        objects = c_models.MerchantCode.objects

    for result in list(objects.values(column).distinct()):
        array.append(result[column])

    return array


def get_row_and_id(model, column):
    logger.info('Requested ' + column + ' from ' + model)
    objects = None
    array = {}
    if model == 'MerchantCode':
        objects = c_models.MerchantCode.objects

    for result in list(objects.values(column, 'id').distinct()):
        array[result['id']] = result[column]

    return array

