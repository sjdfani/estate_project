# Generated by Django 3.2 on 2023-01-19 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estate', '0005_home_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='home_history',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
