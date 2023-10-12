from django.db import models
from django_mysql.models import ListCharField

class ResultItemsModel(models.Model):
    item_name = models.CharField(max_length=100)
    item_price = models.IntegerField(max_length=100)
    item_code = models.CharField(max_length=100)
    image_urls = ListCharField(models.CharField(max_length=100),size=3, max_length=(4 * 100))
    ranking = models.IntegerField(null=True)
    
    def __str__(self):
        return self.item_name
    
