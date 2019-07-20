from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=30,unique=True)
    img = models.ImageField(upload_to='img', null=True, blank=True, default=r'img/turtle1.jpg')
    salt = models.CharField(max_length=20, null=True)
    regist_time = models.CharField(max_length=32, null=True)
    access_time = models.CharField(max_length=32, null=True)
    reset_password_salt = models.CharField(max_length=64, null=True, blank=True)
    reset_time = models.DateTimeField(null=True)
