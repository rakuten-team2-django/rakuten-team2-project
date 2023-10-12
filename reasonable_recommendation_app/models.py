from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    birthday = models.DateField()
    last_login = models.DateTimeField(null=True, blank=True)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.username
    
class Discounted_Items(models.Model):
    product_id=models.CharField(max_length=100,blank=True, null=True)
    product_name=models.CharField(max_length=200,blank=True, null=True)
    product_price=models.DecimalField(max_digits=10,decimal_places=2)
    productimg_url=models.URLField(null=True)
    product_link = models.URLFIELD(null=True)
    product_rank = models.IntegerField(null=True)

    
    def _str_(self):
        return self.product_name
