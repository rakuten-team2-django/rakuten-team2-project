# Generated by Django 4.2.5 on 2023-09-28 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reasonable_recommendation_app', '0009_discounted_items_productimg_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discounted_items',
            name='productimg_url',
            field=models.URLField(null=True),
        ),
    ]
