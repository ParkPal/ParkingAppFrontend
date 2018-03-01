from django.db import models

import datetime

from django.utils import timezone

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Host(models.Model):
    lot_name = models.CharField(max_length=200)
    host_name = models.CharField(default = '',max_length = 60)
    owner = models.CharField(default= '',max_length = 60)
    last_connect = models.DateTimeField(default=timezone.now())
    spot_count = models.IntegerField(default=0)
    spot_limit = models.IntegerField(default=0)
    open = models.BooleanField(default = False)
    current_capacity = models.DecimalField(default=0, max_digits = 5, decimal_places = 5)

    def __str__(self):
        return self.lot_name

class Node(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    in_use = models.BooleanField(default = False)
    disabled = models.BooleanField(default = False)
    last_connect = models.DateTimeField(default=timezone.now())
    ip_addr = models.CharField(default = '', max_length=15)
    def __str__(self):
        return self.ip_addr
    def is_occupied(self):
        return self.in_use



