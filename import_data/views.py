import logging
import json
from datetime import datetime
from pandas import read_csv
from django.shortcuts import render
from django.views.generic import FormView
from django.http import JsonResponse

from . import forms
from categories import models as c_models
from operations import models as o_models


logger = logging.getLogger('django')


class ImportCsvView(FormView):
    form_class = forms.ImportFileForm
    template_name = 'import_data/import_csv.html'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST['action'] == 'get_mcc':
                return JsonResponse(get_column('MerchantCode', 'name'), safe=False)
            if request.POST['action'] == 'import_table':
                non_inserted = ImportTable(request.POST['data']).insert()
                if non_inserted is not None:
                    return JsonResponse(non_inserted, safe=False)
                else:
                    return JsonResponse({'ok': 'ok'})
        else:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            file = request.FILES['file']
            if form.is_valid():
                table = parse_csv(file)
                table = find_mcc_for_desc(table)
                return render(request, 'import_data/import_table.html', {'table': table})
            else:
                return self.form_invalid(form)


class ImportTable(object):
    def __init__(self, table):
        self.operations_array = json.loads(table)
        self.insert_result = {'inserted': [], 'not_inserted': []}

    def insert(self):
        for item in self.operations_array:
            result = self.insert_operation(self, item)
            print(result)
            if result['result'] == 1:
                self.insert_result['inserted'].append(result['id'])
            else:
                self.insert_result['not_inserted'].append(result['id'])
        return self.insert_result

    @staticmethod
    def insert_currency(currency):
        result = c_models.Currency.objects.get_or_create(code__exact=currency, defaults={'code': currency})
        if result[1]:
            logger.info('New currency was added: ' + currency)
        pk = c_models.Currency.objects.filter(code__exact=currency).values('id')[0]['id']
        return pk

    @staticmethod
    def insert_account(account):
        result = o_models.Account.objects.get_or_create(number__exact=account, defaults={'number': account})
        if result[1]:
            logger.info('New account was added: ' + account)
        pk = o_models.Account.objects.filter(number__exact=account).values('id')[0]['id']
        return pk

    @staticmethod
    def insert_desc(desc):
        result = c_models.Description.objects.get_or_create(name__exact=desc, defaults={'name': desc})
        if result[1]:
            logger.info('New description was added: ' + desc)
        pk = c_models.Description.objects.filter(name__exact=desc).values('id')[0]['id']
        return pk

    @staticmethod
    def insert_merchant_code(mcc):
        result = c_models.MerchantCode.objects.get_or_create(name__exact=mcc, defaults={'name': mcc})
        if result[1]:
            logger.info('New merchant code was added: ' + mcc)
        pk = c_models.MerchantCode.objects.filter(name__exact=mcc).values('id')[0]['id']
        return pk

    @staticmethod
    def insert_operation(self, _item):
        date = datetime.strptime(_item['date'], '%d.%m.%Y %H:%M:%S')
        account = o_models.Account.objects.get(id__exact=self.insert_account(_item['account']))
        operation_cur = c_models.Currency.objects.get(id__exact=self.insert_currency(_item['operation_cur']))
        bargain_cur = c_models.Currency.objects.get(id__exact=self.insert_currency(_item['bargain_cur']))
        description = c_models.Description.objects.get(id__exact=self.insert_desc(_item['description']))
        merchant_code = c_models.MerchantCode.objects.get(id__exact=self.insert_merchant_code(_item['merchant_code']))
        result = o_models.Operation.objects.get_or_create(date__exact=date,
                                                          merchant_code__exact=merchant_code,
                                                          description__exact=description,
                                                          defaults={
                                                              'date': date,
                                                              'account': account,
                                                              'status': _item['status'],
                                                              'operation_sum': _item['operation_sum'],
                                                              'operation_cur': operation_cur,
                                                              'bargain_sum': _item['bargain_sum'],
                                                              'bargain_cur': bargain_cur,
                                                              'merchant_code': merchant_code,
                                                              'description': description,
                                                              'comment': _item['comment']
                                                          })
        if result[1]:
            logger.info('New operation was added: ' + json.dumps(_item, ensure_ascii=False, separators=(',', ':')))
            return {'result': 1, 'id': _item['id']}
        elif result[0].pk:
            logger.warning('Operation was not added: ' + json.dumps(_item, ensure_ascii=False, separators=(',', ':')) +
                           '. Duplicates operation id: ' + str(result[0].pk))
            return {'result': 0, 'id': _item['id']}
        else:
            logger.warning('Operation was not added: ' + json.dumps(_item, ensure_ascii=False, separators=(',', ':')))
            return {'result': 0, 'id': _item['id']}


def parse_csv(csv_file):
    table = read_csv(csv_file, encoding='cp1251',  delimiter=';', keep_default_na=False, header=0, decimal=",",
                     names=['date', 'bargain_date', 'account', 'status', 'operation_sum', 'operation_cur',
                            'bargain_sum', 'bargain_cur', 'cashback', 'merchant_code', 'mcc', 'description',
                            'bonuses'])

    table = table.iloc[::-1].T.to_dict()
    return table.values


def find_mcc_for_desc(table):
    for row in table():
        description = c_models.Description.objects.get(name=row['description'])
        if description.merchant_code:
            row['merchant_code_matched'] = description.merchant_code
        else:
            row['merchant_code_matched'] = row['merchant_code']

    return table


def get_column(model, column):
    logger.info('Requested ' + column + ' from ' + model)
    objects = None
    array = []
    if model == 'Description':
        objects = c_models.Description.objects
    if model == 'MerchantCode':
        objects = c_models.MerchantCode.objects

    for result in list(objects.values(column).distinct()):
        array.append(result[column])

    return array
