from operator import eq
from statistics import mode
from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date

from django.contrib.auth.models import User  # Required to assign User as a borrower

class Manufactory (models.Model):
    name = models.CharField(max_length=200, help_text="")
    country = models.CharField(max_length=200, help_text="")

    def __str__(self):
        return self.name

class Item_type(models.Model):
    name = models.CharField(max_length=200, help_text="")

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=320, help_text="")
    inventory_number = models.CharField(max_length=32)
    item_type = models.ForeignKey('Item_type', on_delete=models.SET_NULL, null = True)
    manufactory = models.ForeignKey('Manufactory', on_delete=models.SET_NULL, null = True)
    manufactory_number = models.CharField(max_length=48)
    equipment = models.TextField(max_length= 1024)
    production_date = models.DateField()
    cost = models.IntegerField()
    use_date = models.DateField()
    registrated_number = models.CharField(max_length=320)
    properties = models.TextField(max_length=3200)
    responsible_person = models.ForeignKey('User', on_delete=models.SET_NULL, null = True)
    image = models.CharField(max_length=128)

    ITEM_STATUS = (
        ('i', 'in_use'),
        ('r', 'repair'),
        ('t', 'taken')
    )

    status = models.CharField(max_length=1, choices=ITEM_STATUS, blank= True, default='i', help_text='')
    person_temp = models.ForeignKey('User', on_delete=models.SET_NULL, null = True)
    class Meta:
        ordering = ['name', 'item_type']

    def get_absolute_url(self):
        return reverse('item-detail', args = [str(self.id)])

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    room = models.CharField(max_length=10)
    department = models.CharField(max_length=100)
    telephone = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    image = models.CharField(max_length=128)
    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('user-detail', args = [str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)

class Transfer(models.Model):
    item = models.ForeignKey('Item', on_delete=models.SET_NULL, null = True)
    borrower = models.ForeignKey('User', on_delete=models.SET_NULL, null = True)
    satrt_date = models.DateField(auto_now = True)

    TRANSFER_STATUS = (
        ('c', 'created'),
        ('s', 'Request sent'),
        ('a', 'allowed'),
        ('r', 'refuse'),
        ('e', 'returned/transfer ended')
    )

    status = models.CharField(max_length=1, choices=TRANSFER_STATUS, blank= True, default='c', help_text='')