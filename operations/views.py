import logging
from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.core.paginator import Paginator
from django.http import JsonResponse
from operations import (models as o_models, forms)
from categories import models as c_models
from import_data import views as i_views

logger = logging.getLogger('django')


class OperationListView(ListView):
    model = o_models.Operation
    paginate_by = 50

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        if request.is_ajax():
            if request.POST['action'] == 'delete_operation':
                result = delete_object('Operation', {'id': request.POST['data'].replace('"', "")})
                return JsonResponse({'result': result})
            if request.POST['action'] == 'update_operation':
                result = update_object('Operation', {'id': request.POST['id']},
                                       {request.POST['field']: request.POST['new_value']})
                return JsonResponse({'rows_updated': result})
            if request.POST['action'] == 'add_operation':
                insert_result = i_views.ImportTable(request.POST['data']).insert()
                return JsonResponse(insert_result, safe=False)



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

        # print(filter_args)
        return filter_args

    def get_queryset(self):
        filter_args = self.get_filters()

        if self.request.GET.get('orderby') == 'ASC':
            new_context = self.model.objects.filter(
                **filter_args
            ).order_by('date')
        else:
            new_context = self.model.objects.filter(
                **filter_args
            ).order_by('-date')

        return new_context

    def get_context_data(self, **kwargs):
        context = super(OperationListView, self).get_context_data(**kwargs)
        context['model_name'] = self.model.__name__
        context['status'] = get_column('Operation', 'status')
        context['merchant_code'] = get_row_and_id('MerchantCode', 'name')
        context['category'] = get_row_and_id('Category', 'name')
        context['type'] = get_row_and_id('Type', 'name')
        context['account'] = get_row_and_id('Account', 'number')
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
                                                                      'page_obj': page_obj,
                                                                      'merchant_code': get_row_and_id('MerchantCode',
                                                                                                      'name')})
        return super().get(request, *args, **kwargs)


def update_object(model, filters, updates):
    logger.info('Requested update for ' + model)
    logger.info('Objects to update: ')
    for k, v in filters.items():
        logger.info('where ' + k + ' = ' + str(v))
    for k, v in updates.items():
        logger.info('Field to update: ' + k + ' to ' + str(v))
    objects = None
    if model == 'MerchantCode':
        objects = c_models.MerchantCode.objects
    if model == 'Operation':
        objects = o_models.Operation.objects

    result = objects.filter(**filters).update(**updates)
    logger.info('Updated number of objects: ' + str(result))
    return result


def delete_object(model, filters):
    logger.warning('Requested delete from ' + model)
    logger.warning('Objects to delete: ')
    for k, v in filters.items():
        logger.warning('where ' + k + ' = ' + str(v))
    objects = None
    if model == 'Operation':
        objects = o_models.Operation.objects

    result = objects.filter(**filters).delete()[1]
    for k, v in result.items():
        logger.warning('Deleted from ' + k + '. Number of items: ' + str(v))
    return result


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
    if model == 'Account':
        objects = o_models.Account.objects

    for result in list(objects.values(column, 'id').order_by(column).distinct()):
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
