import logging
from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.core.paginator import Paginator
from operations import (models as o_models, forms)
from categories import models as c_models

logger = logging.getLogger('django')


class OperationListView(ListView):
    model = o_models.Operation
    paginate_by = 50

    def get_filters(self):
        # print(self.request.GET)
        filter_args = {}
        filter_args['status__in'] = self.request.GET.getlist('status[]') \
            if len(self.request.GET.getlist('status[]')) > 0 else ['OK']
        if self.request.GET.get('date_from'):
            filter_args['date__gte'] = self.request.GET.get('date_from')
        if self.request.GET.get('date_to'):
            filter_args['date__lte'] = self.request.GET.get('date_to') + ' 23:59:59'
        if self.request.GET.get('merchant_code[]') \
                or self.request.GET.get('category[]') \
                or self.request.GET.get('type[]'):

            filter_arr = []
            if self.request.GET.get('category[]'):
                mcc_cat = get_foreign_objects_by_filter('MerchantCode',
                                                        {'category__in': self.request.GET.getlist('category[]')})
                for value in mcc_cat:
                    filter_arr.append(value)

            if self.request.GET.get('type[]'):
                cat_type = get_foreign_objects_by_filter('Category',
                                                         {'type__in': self.request.GET.getlist('type[]')})
                mcc_cat = get_foreign_objects_by_filter('MerchantCode',
                                                        {'category__in': cat_type})
                for value in mcc_cat:
                    filter_arr.append(value)

            if self.request.GET.get('merchant_code[]'):
                for value in self.request.GET.getlist('merchant_code[]'):
                    filter_arr.append(value)

            filter_args['merchant_code__in'] = filter_arr

        print(filter_args)
        return filter_args

    def get_queryset(self):
        filter_args = self.get_filters()

        if self.request.GET.get('orderby') == 'ASC':
            new_context = o_models.Operation.objects.filter(
                **filter_args
            ).order_by('date')
        else:
            new_context = o_models.Operation.objects.filter(
                **filter_args
            ).order_by('-date')

        return new_context

    def get_context_data(self, **kwargs):
        context = super(OperationListView, self).get_context_data(**kwargs)
        context['status'] = get_column('Operation', 'status')
        context['merchant_code'] = get_row_and_id('MerchantCode', 'name')
        context['category'] = get_row_and_id('Category', 'name')
        context['type'] = get_row_and_id('Type', 'name')
        context['orderby'] = self.request.GET.get('orderby')
        return context


class OperationsView(OperationListView):
    template_name = 'operations/operations.html'

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('filter_applied'):
            operation_list = self.get_queryset()

            paginator = Paginator(operation_list, 50)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            operation_list_page = paginator.page(page_number).object_list if True else ''

            return render(request, 'operations/operation_list.html', {'operation_list': operation_list_page,
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
    if model == 'Category':
        objects = c_models.Category.objects
    if model == 'Type':
        objects = c_models.Type.objects

    for result in list(objects.values(column, 'id').distinct()):
        array[result['id']] = result[column]

    return array


def get_foreign_objects_by_filter(model, filter_args):
    # print(filter_args)
    objects = None
    array = []
    if model == 'MerchantCode':
        objects = c_models.MerchantCode.objects
    if model == 'Category':
        objects = c_models.Category.objects

    for result in list(objects.filter(**filter_args).values('id').distinct()):
        array.append(result['id'])

    return array
