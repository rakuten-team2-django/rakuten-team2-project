# Generated by Django 3.2.21 on 2023-09-27 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reasonable_recommendation_app', '0003_user_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_login',
        ),
    ]
