# Generated by Django 3.2.21 on 2023-09-27 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reasonable_recommendation_app', '0002_user_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
