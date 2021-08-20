from django.db import models

from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField('Название', primary_key = True, max_length=80)
    amount = models.IntegerField('Количество', default=0)
    used_today = models.IntegerField('Использовано', default=0)
    clinic = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def set_amount(self, num):
        self.used_today = 0
        self.amount = num
        
    def add_amount(self, num):
        self.used_today = 0
        self.amount += num
    
    def remove_amount(self, num):
        self.used_today += num
        self.amount -= num


class Partner(models.Model):
    id = models.IntegerField('ID', primary_key = True)
    name = models.CharField('Имя', max_length=25)
    surname = models.CharField('Фамилия', max_length=25)
    payed = models.IntegerField('Прибыль', default=0)
    bill = models.IntegerField('Долг', default=0)
    client_num = models.IntegerField('Количество клиентов', default=0)
    clinic = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    
    def pay(self, num):
        self.payed += num
        self.bill -= num
        if self.bill < 0:
            self.bill = 0
    
    def add_bill(self, num):
        self.bill += num
    

class Client(models.Model):
    id = models.IntegerField('ID', primary_key = True)
    name = models.CharField('Имя', max_length=25)
    surname = models.CharField('Фамилия', max_length=25)
    isAdult = models.BooleanField('Взрослый', default=True)
    payed = models.IntegerField('Оплачено', default=0)
    bill = models.IntegerField('Долг', default=0)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    
    def pay(self, num):
        self.payed += num
        self.bill -= num
        if self.bill < 0:
            self.bill = 0
    
    def add_bill(self, num):
        self.bill += num
    

class Task(models.Model):
    name = models.CharField('Название', primary_key = True, max_length=80)
    desc = models.TextField('Количество')
    made = models.BooleanField('Выполнено', default=True)
    clinic = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    def complete(self):
        self.made = True
        
