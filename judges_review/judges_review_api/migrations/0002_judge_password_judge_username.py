# Generated by Django 5.0.3 on 2024-03-19 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judges_review_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='judge',
            name='password',
            field=models.CharField(default='123456', max_length=255),
        ),
        migrations.AddField(
            model_name='judge',
            name='username',
            field=models.CharField(default='123456', max_length=255),
        ),
    ]
