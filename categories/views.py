import logging
from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.http import JsonResponse
from django.core.paginator import Paginator
from categories import (models as c_models, forms)
from operations import models as o_models

logger = logging.getLogger('django')


class TypeListView(ListView):
    model = c_models.Type


class CategoryListView(ListView):
    model = c_models.Category

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        if request.is_ajax():
            if request.POST['action'] == 'delete_object_replace':
                ops_update = update_object('MerchantCode', {'category_id': request.POST['id'].replace('"', "")},
                                           {request.POST['field']: request.POST['new_value'].replace("'", "")})
                result = delete_object('Category', {'id': request.POST['id'].replace('"', "")})
                return JsonResponse({'merchant_codes_updated': ops_update, 'result': result})
            if request.POST['action'] == 'update_object':
                result = update_object('Category', {'id': request.POST['id']},
                                       {request.POST['field']: request.POST['new_value']})
                return JsonResponse({'rows_updated': result})

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['object_list'] = self.model.objects.all().order_by('name')
        context['model_name'] = self.model.__name__
        context['comparison_list'] = c_models.Type.objects.all().order_by('name')
        return context


class MerchantCodeListView(ListView):
    model = c_models.MerchantCode

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        if request.is_ajax():
            if request.POST['action'] == 'delete_object_replace':
                ops_update = update_object('Operation', {'merchant_code_id': request.POST['id'].replace('"', "")},
                                           {request.POST['field']: request.POST['new_value'].replace("'", "")})
                result = delete_object('MerchantCode', {'id': request.POST['id'].replace('"', "")})
                return JsonResponse({'operations_updated': ops_update, 'result': result})
            if request.POST['action'] == 'update_object':
                result = update_object('MerchantCode', {'id': request.POST['id']},
                                       {request.POST['field']: request.POST['new_value']})
                return JsonResponse({'rows_updated': result})

    def get_context_data(self, **kwargs):
        context = super(MerchantCodeListView, self).get_context_data(**kwargs)
        context['object_list'] = self.model.objects.all().order_by('name')
        context['model_name'] = self.model.__name__
        context['comparison_list'] = c_models.Category.objects.all().order_by('name')
        return context


class DescriptionListView(ListView):
    model = c_models.Description
    paginate_by = 50

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        if request.is_ajax():
            if request.POST['action'] == 'delete_object_replace':
                ops_update = update_object('Operation', {'description_id': request.POST['id'].replace('"', "")},
                                           {request.POST['field']: request.POST['new_value'].replace("'", "")})
                result = delete_object('Description', {'id': request.POST['id'].replace('"', "")})
                return JsonResponse({'operations_updated': ops_update, 'result': result})
            if request.POST['action'] == 'update_object':
                result = update_object('Description', {'id': request.POST['id']},
                                       {request.POST['field']: request.POST['new_value']})
                return JsonResponse({'rows_updated': result})

    def get_filters(self):
        print(self.request.GET)
        filter_args = {}
        filter_args['name__contains'] = self.request.GET.get('name') \
            if self.request.GET.get('name') else ''

        print(filter_args)
        return filter_args

    def get_queryset(self):
        filter_args = self.get_filters()

        new_context = self.model.objects.filter(
            **filter_args
        ).order_by('-merchant_code_id', '-id')

        return new_context

    def get_comparison_list(self):
        return c_models.MerchantCode.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super(DescriptionListView, self).get_context_data(**kwargs)
        context['model_name'] = self.model.__name__
        context['comparison_list'] = self.get_comparison_list()
        return context


class DescriptionsView(DescriptionListView):
    template_name = 'categories/descriptions.html'

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('filter_applied'):
            object_list = self.get_queryset()
            comparison_list = self.get_comparison_list()

            paginator = Paginator(object_list, 50)
            page_number = self.request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            object_list_page = paginator.page(page_number).object_list if True else ''

            return render(request, 'categories/description_list.html', {'object_list': object_list_page,
                                                                        'page_obj': page_obj,
                                                                        'comparison_list': comparison_list})
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
    if model == 'Category':
        objects = c_models.Category.objects
    if model == 'Description':
        objects = c_models.Description.objects

    result = objects.filter(**filters).update(**updates)
    logger.info('Updated number of objects: ' + str(result))
    return result


def delete_object(model, filters):
    logger.warning('Requested delete from ' + model)
    logger.warning('Objects to delete: ')
    for k, v in filters.items():
        logger.warning('where ' + k + ' = ' + str(v))
    objects = None
    if model == 'MerchantCode':
        objects = c_models.MerchantCode.objects
    if model == 'Category':
        objects = c_models.Category.objects
    if model == 'Description':
        objects = c_models.Description.objects

    result = objects.filter(**filters).delete()[1]
    for k, v in result.items():
        logger.warning('Deleted from ' + k + '. Number of items: ' + str(v))
    return result
