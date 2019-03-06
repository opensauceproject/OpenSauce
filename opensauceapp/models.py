from django.db import models
from django.db.models.signals import post_save, post_delete

class Category(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Sauce(models.Model):
    id=models.AutoField(primary_key=True)
    question=models.CharField(max_length=200)
    answer=models.CharField(max_length=200)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty=models.IntegerField()
    media_type=models.IntegerField()


