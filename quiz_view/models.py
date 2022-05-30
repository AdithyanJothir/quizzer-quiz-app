from enum import unique
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    no_of_cards = models.IntegerField(null=True,blank=True)
    no_of_people_answred = models.IntegerField(null=True,blank=True)
    unique_url = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name

class Card(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    question = models.TextField(max_length=200)
    answer = models.CharField(max_length=50)
    select = models.BooleanField()

class Answerer(models.Model):
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    correct_answer = models.IntegerField()
    name = models.CharField(max_length=20)

    