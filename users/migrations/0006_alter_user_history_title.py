# Generated by Django 3.2 on 2023-01-19 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_history_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_history',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
