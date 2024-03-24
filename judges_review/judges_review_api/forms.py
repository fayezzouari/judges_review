from django import forms
from django.contrib.auth.models import User, Group
from .models import Project


class AddProject(forms.Form):
    id = forms.CharField(label='Id')


class AssignJudgeProject(forms.Form):
    project_id= forms.ModelChoiceField(queryset=Project.objects.all())
    judge = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Judge'))


class GradeProject(forms.Form):
    precision = forms.FloatField()
    presentation = forms.FloatField()
    procres = forms.FloatField()
    orgim = forms.FloatField()
    feasibility = forms.FloatField()


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ProjectSearchForm(forms.Form):
    project_id = forms.CharField(label='Project ID', max_length=100)