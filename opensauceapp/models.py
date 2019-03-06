from django.db import models
from django.db.models.signals import post_save, post_delete
'''
class BaseModel(models.Model):
    class Meta:
        abstract = True  # specify this model as an Abstract Model
        app_label = 'wdland'
    class Sauce:
        citation=models.CharField(max_length=200)

    class Category:
        name=models.CharField(max_length=200)
        description=models.TextField()
        def __str__(self):
            return self.name
'''

class Category(models.Model):
    id=models.AutoField(primary_key=True)
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


