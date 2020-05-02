import logging
from django.db import models

logger = logging.getLogger('django')


class Type(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    type = models.ForeignKey('categories.Type', on_delete=models.PROTECT, null=True, related_name='type')

    def __str__(self):
        return self.name


class MerchantCode(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey('categories.Category', on_delete=models.PROTECT, null=True, related_name='category')

    def __str__(self):
        return self.name


class Description(models.Model):
    name = models.CharField(max_length=256)
    merchant_code = models.ForeignKey('categories.MerchantCode', on_delete=models.PROTECT, null=True,
                                      related_name='descmcc')

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=8, unique=True)

    def __str__(self):
        return self.code
