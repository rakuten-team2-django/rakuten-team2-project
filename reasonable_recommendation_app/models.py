from django.db import models
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)



    email = models.CharField(max_length=200)
    birthday = models.DateField()

    def __str__(self):
        return self.username




