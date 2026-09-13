from django.db import models

from app.domain.entities.enums import TransactionType

TRANSACTION_TYPE_CHOICES = [(t.value, t.value) for t in TransactionType]


class AccountModel(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    balance = models.IntegerField(default=0)


class TransactionModel(models.Model):
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.IntegerField()
    origin_id = models.CharField(max_length=255, null=True, blank=True)
    destination_id = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
