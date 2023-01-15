# Generated by Django 3.2 on 2023-01-15 21:44

from django.db import migrations, models
import django.utils.timezone
import users.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='Username')),
                ('fullname', models.CharField(max_length=50, verbose_name='Fullname')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='Phone Number')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('is_manager', models.BooleanField(default=False, verbose_name='Is Manager')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is Admin')),
                ('is_adviser', models.BooleanField(default=False, verbose_name='Is Adviser')),
                ('is_user', models.BooleanField(default=False, verbose_name='Is User')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', users.manager.CustomUserManager()),
            ],
        ),
    ]
