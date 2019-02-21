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

class Sauce(models.Model):
    citation=models.CharField(max_length=200)

class Category(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    def __str__(self):
        return self.name
