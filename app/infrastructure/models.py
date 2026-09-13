from django.db import models

class TransactionModel(models.Model):
    origin_id = models.CharField(max_length=255)
    destination_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

class AccountModel(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)