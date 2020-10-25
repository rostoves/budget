import logging
import json
from datetime import datetime, timedelta
from pandas import read_csv, date_range
from django.shortcuts import render
from django.views.generic import FormView
from django.http import JsonResponse
from django.db.models import Sum, Max
from django.db.models.functions import TruncDate
from django.core.exceptions import ObjectDoesNotExist

from . import forms
from categories import models as c_models
from operations import models as o_models


logger = logging.getLogger('django')


class ImportCsvView(FormView):
    form_class = forms.ImportFileForm
    template_name = 'import_data/import_csv.html'
    plan_desc_id = 2998

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.POST['action'] == 'get_mcc':
                return JsonResponse(get_column('MerchantCode', 'name', {'active': True}), safe=False)
            if request.POST['action'] == 'import_table':
                insert_result = ImportTable(request.POST['data']).insert()
                delete_object('Operation', {'description_id__exact': self.plan_desc_id,
                                            'date__lte': datetime.today() + timedelta(days=1)})

                UpdateRegularPlans(self.plan_desc_id).update_regular_operations()
                return JsonResponse(insert_result, safe=False)
        else:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            file = request.FILES['file']
            if form.is_valid():
                table = self.parse_csv(file)
                table = self.find_mcc_for_desc(table)
                return render(request, 'import_data/import_table.html', {'table': table})
            else:
                return self.form_invalid(form)

    @staticmethod
    def parse_csv(csv_file):
        table = read_csv(csv_file, encoding='cp1251', delimiter=';', keep_default_na=False, header=0,
                         decimal=",",
                         names=['date', 'bargain_date', 'account', 'status', 'operation_sum', 'operation_cur',
                                'bargain_sum', 'bargain_cur', 'cashback', 'merchant_code', 'mcc', 'description',
                                'bonuses', 'round', 'round_sum'])

        table = table.iloc[::-1].T.to_dict()
        return table.values

    @staticmethod
    def find_mcc_for_desc(table):
        for row in table():
            try:
                description = c_models.Description.objects.get(name=row['description'])
                if description.merchant_code is not None:
                    row['merchant_code_matched'] = description.merchant_code
                    logger.info("Found Merchant Code " + str(description.merchant_code) +
                                " for Description: " + str(description))
                else:
                    row['merchant_code_matched'] = row['merchant_code']
                    logger.info("No specific Merchant Code for Description: " + str(description) +
                                ". Will keep: " + row['merchant_code_matched'])
            except ObjectDoesNotExist:
                row['merchant_code_matched'] = row['merchant_code']

        return table


class ImportTable(object):
    def __init__(self, table):
        self.operations_array = json.loads(table)
        self.insert_result = {'inserted': [], 'not_inserted': []}

    def insert(self):
        logger.info('Got array for insert. Number of operations: ' + str(len(self.operations_array)))
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
        logger.info('Looking for currency: ' + currency)
        result = c_models.Currency.objects.get_or_create(code__exact=currency, defaults={'code': currency})
        if result[1]:
            logger.info('New currency was added: ' + currency)
        pk = c_models.Currency.objects.filter(code__exact=currency).values('id')[0]['id']
        return pk

    @staticmethod
    def insert_account(account):
        logger.info('Looking for account: ' + account)
        result = o_models.Account.objects.get_or_create(number__exact=account, defaults={'number': account})
        if result[1]:
            logger.info('New account was added: ' + account)
        pk = o_models.Account.objects.filter(number__exact=account).values('id')[0]['id']
        return pk

    @staticmethod
    def insert_desc(desc):
        logger.info('Looking for description: ' + desc)
        result = c_models.Description.objects.get_or_create(name__exact=desc, defaults={'name': desc})
        if result[1]:
            logger.info('New description was added: ' + desc)
        pk = c_models.Description.objects.filter(name__exact=desc).values('id')[0]['id']
        return pk

    @staticmethod
    def insert_merchant_code(mcc):
        logger.info('Looking for merchant code: ' + mcc)
        result = c_models.MerchantCode.objects.get_or_create(name__exact=mcc, defaults={'name': mcc})
        if result[1]:
            logger.info('New merchant code was added: ' + mcc)
        pk = c_models.MerchantCode.objects.filter(name__exact=mcc).values('id')[0]['id']
        return pk

    @staticmethod
    def insert_operation(self, _item):
        logger.info('Trying to add new operation. ID in insert array: ' + str(_item['id']))
        account = o_models.Account.objects.get(id__exact=self.insert_account(_item['account']))
        operation_cur = c_models.Currency.objects.get(id__exact=self.insert_currency(_item['operation_cur']))
        bargain_cur = c_models.Currency.objects.get(id__exact=self.insert_currency(_item['bargain_cur']))
        description = c_models.Description.objects.get(id__exact=self.insert_desc(_item['description']))
        merchant_code = c_models.MerchantCode.objects.get(id__exact=self.insert_merchant_code(_item['merchant_code']))
        if _item['manual_insert']:
            date = datetime.strptime(_item['date'][:-1], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(hours=3)
            merchant_code_original = merchant_code
        else:
            date = datetime.strptime(_item['date'], '%d.%m.%Y %H:%M:%S')
            merchant_code_original = c_models.MerchantCode.objects.get(id__exact=self.insert_merchant_code(_item['merchant_code_original']))
        result = o_models.Operation.objects.get_or_create(date__exact=date,
                                                          bargain_sum__exact=_item['bargain_sum'],
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
                                                              'merchant_code_original': merchant_code_original,
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


class UpdateRegularPlans(object):
    model = o_models.Operation
    today = datetime.today()
    today = datetime.date(today)

    def __init__(self, regular_desc_id):
        self.plan_desc_id = regular_desc_id
        self.period_avg_calc = 180
        self.plan_period = 364
        self.regular_type_id = 2
        self.plan_status = 'PLAN'
        self.plan_cur = 1079
        self.plan_account = 24
        self.regulars = self.get_queryset()

    def get_queryset(self):
        result = self.model.objects.filter(merchant_code__category__type=self.regular_type_id,
                                           date__date__gte=self.today-timedelta(days=self.period_avg_calc))\
            .exclude(description_id__exact=self.plan_desc_id).values('merchant_code', 'merchant_code__name')\
            .annotate(bargain_sum=Sum('bargain_sum'))

        for entry in result:
            entry['bargain_sum'] = round(entry['bargain_sum']/self.period_avg_calc, 2)
            logger.info("Average sum for "+entry['merchant_code__name']+" operations: "+str(entry['bargain_sum']))

        return result

    def update_regular_operations(self):
        current_planned_date = self.model.objects.filter(description_id__exact=self.plan_desc_id).aggregate(date=TruncDate(Max('date'), tzinfo='UTC'))['date']
        logger.info("Latest date with planned operations: " + str(current_planned_date))
        period_for_planning = self.plan_period - (current_planned_date - self.today).days

        date_list = date_range(current_planned_date + timedelta(days=1), periods=period_for_planning, normalize=True).tolist()
        if date_list:
            logger.info("Number of days for planning: " + str(len(date_list)))
            for date in date_list:
                logger.info("New date for planning: : " + str(date))
        else:
            logger.info("No dates for planning")

        for record in self.regulars:
            update_object('Operation', {'merchant_code_id': record['merchant_code'], 'description_id': self.plan_desc_id},
                          {'bargain_sum': record['bargain_sum']})

            if date_list:
                objs = []
                for date in date_list:
                    objs.append(self.model(date=date,
                                           account_id=self.plan_account,
                                           status=self.plan_status,
                                           operation_sum=record['bargain_sum'],
                                           operation_cur_id=self.plan_cur,
                                           bargain_sum=record['bargain_sum'],
                                           bargain_cur_id=self.plan_cur,
                                           merchant_code_id=record['merchant_code'],
                                           description_id=self.plan_desc_id))

                result = self.model.objects.bulk_create(objs)
                logger.info("Planned operations: " + str(len(result)) + " for " + record['merchant_code__name'])


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


def get_column(model, column, filters):
    logger.info('Requested ' + column + ' from ' + model)
    objects = None
    array = []
    if model == 'Description':
        objects = c_models.Description.objects
    if model == 'MerchantCode':
        objects = c_models.MerchantCode.objects.filter(**filters)
    if model == 'Operation':
        objects = o_models.Operation.objects

    for result in list(objects.values(column).distinct()):
        array.append(result[column])

    return array
