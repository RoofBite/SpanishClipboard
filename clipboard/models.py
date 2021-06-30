from django.db import models
from django.contrib.auth.models import User

class Word(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank= True)
    polish_word=models.CharField(max_length=200,null=True,blank=True)
    spanish_word=models.CharField(max_length=200,null=True,blank=True)
    etymology=models.CharField(max_length=200,null=True,blank=True)
    notes=models.TextField(max_length=2000,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.polish_word + " - "+self.spanish_word)