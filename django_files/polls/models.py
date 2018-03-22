from django.db import models

import datetime

from django.utils import timezone
from django.contrib.auth.models import User

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

    lotName = models.CharField(unique = True, max_length=64)
    owner = models.ForeignKey(User,unique = False, on_delete=models.CASCADE )
    lastConnect = models.DateTimeField(default=timezone.now())
    spotCount = models.IntegerField(default=0)
    spotlimit = models.IntegerField(default=0)
    open = models.BooleanField(default = False)
    currentCapacity = models.DecimalField(default=0, max_digits = 5, decimal_places = 3)

    def __str__(self):
        return self.lotName

class Node(models.Model):
    host = models.ForeignKey(Host, unique = False, on_delete=models.CASCADE)
    inUse = models.BooleanField(default = False)
    disabled = models.BooleanField(default = False)
    lastConnect = models.DateTimeField(default=timezone.now())
    ipAddr = models.CharField(default = '', max_length=15)
    def __str__(self):
        return self.ipAddr
    def is_occupied(self):
        return self.inUse



