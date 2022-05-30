from tkinter import CASCADE
from django.db import models
from django.forms import CharField
from django.contrib.auth.models import User

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=20)
    no_of_questions = models.IntegerField()

    def __str__(self):
        return self.name