# Generated by Django 4.1.1 on 2023-05-07 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_todo_todoid'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='homeworkId',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
