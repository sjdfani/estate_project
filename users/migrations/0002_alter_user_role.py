# Generated by Django 3.2 on 2023-01-18 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('manager', 'Manager'), ('assistant', 'Assistant'), ('admin', 'Admin'), ('advisor', 'Advisor'), ('user', 'User'), ('none', 'None')], default='none', max_length=9, verbose_name='Role'),
        ),
    ]
