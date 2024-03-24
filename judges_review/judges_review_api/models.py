from django.contrib.auth.models import User, Group
from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Judge(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=255, default="123456")
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    password = models.CharField(max_length=255,default="123456")
    def __str__(self):
        return self.name


class Project(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    def __str__(self):
        return self.id


class Judgement(models.Model):
    id = models.AutoField(primary_key=True),
    project_id = models.ForeignKey(Project, on_delete=models.PROTECT)
    judge = models.ForeignKey(User, on_delete=models.PROTECT)
    score = models.FloatField(default=0)
    def __str__(self):
        return f"Judge: {self.judge} ------ Project: "+ self.project_id.id+ "  Score: "+ str(self.score)

