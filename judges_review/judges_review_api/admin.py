from django.contrib import admin

from .models import Project, Judge, Judgement

# Register your models here.
admin.site.register(Project)
admin.site.register(Judge)
admin.site.register(Judgement)
