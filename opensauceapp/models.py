from django.db import models
from django.db.models.signals import post_save, post_delete

class SauceCategory(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)

class Sauce(models.Model):
    id=models.AutoField(primary_key=True)
    question=models.CharField(max_length=200)
    answer=models.CharField(max_length=200)
    sauce_category=models.ForeignKey(SauceCategory, on_delete=models.CASCADE)
    difficulty=models.IntegerField()
    media_type=models.IntegerField()

class ReportCategory(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=300)

class Report(models.Model):
    id=models.AutoField(primary_key=True)
    sauce=models.ForeignKey(Sauce, on_delete=models.CASCADE)
    additional_informations=models.CharField(max_length=500)

class ReportReportCategory(models.Model):
    id=models.AutoField(primary_key=True)
    report=models.ForeignKey(Report, on_delete=models.CASCADE)
    report_category=models.ForeignKey(ReportCategory, on_delete=models.CASCADE)



