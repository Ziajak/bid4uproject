from django.db import models
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import csv
import datetime
# Create your models here.



class Account_allegro(models.Model):
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class List_bid_allegro(models.Model):
    link = models.CharField(max_length=255)
    bid_date = models.DateTimeField()
    amount =  models.CharField(max_length=10, null=True)
    status = models.CharField(max_length=10, default='Niewykonane')
    account_id = models.ForeignKey(Account_allegro, on_delete=models.CASCADE, null=True)
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)

# class Linked_account(models.Model):
#     first_access_code = models.CharField(max_length=255, null=True)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)



