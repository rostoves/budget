from django.db import models
from django.utils import timezone


class Account(models.Model):
    number = models.CharField(max_length=32)
    name = models.CharField(max_length=32, null=True)
    owner = models.CharField(max_length=32, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.number


class Operation(models.Model):
    date = models.DateTimeField()
    account = models.ForeignKey('operations.Account', on_delete=models.PROTECT, related_name='account')
    status = models.CharField(max_length=32)
    operation_sum = models.DecimalField(max_digits=18, decimal_places=2)
    operation_cur = models.ForeignKey('categories.Currency', on_delete=models.PROTECT, related_name='operation_cur')
    bargain_sum = models.DecimalField(max_digits=18, decimal_places=2)
    bargain_cur = models.ForeignKey('categories.Currency', on_delete=models.PROTECT, related_name='bargain_cur')
    merchant_code = models.ForeignKey('categories.MerchantCode', on_delete=models.PROTECT, related_name='mcc')
    merchant_code_original = models.ForeignKey('categories.MerchantCode', on_delete=models.PROTECT,
                                               related_name='mcc_orig', null=True, blank=True)
    description = models.ForeignKey('categories.Description', on_delete=models.SET_NULL, null=True,
                                    related_name='description')
    comment = models.CharField(max_length=128, blank=True, null=True)
    import_date = models.DateTimeField(default=timezone.now)
