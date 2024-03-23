from django import forms
from django.contrib.auth.models import User, Group
from .models import Project


class AddProject(forms.Form):
    id = forms.CharField(label='Id')
    name = forms.CharField(label='Name', max_length=50)


class AssignJudgeProject(forms.Form):
    project_id= forms.ModelChoiceField(queryset=Project.objects.all())
    judge = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Judge'))


class GradeProject(forms.Form):
    presentation = forms.FloatField()
    prototype = forms.FloatField()
    #business_plan = forms.FloatField()
    idea = forms.FloatField()


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()


class ProjectSearchForm(forms.Form):
    project_id = forms.CharField(label='Project ID', max_length=100)