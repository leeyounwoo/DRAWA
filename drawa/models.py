from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     phone = models.TextField()


class Store(models.Model):
    is_online = models.BooleanField()
    nation = models.TextField(null=True, blank=True)
    location_si = models.TextField(null=True, blank=True)
    location_gu = models.TextField(null=True, blank=True)
    location_dong = models.TextField(null=True, blank=True)
    location_detail = models.TextField(null=True, blank=True)
    homepage_url = models.TextField()
    community_url = models.TextField()
    tel = models.TextField(null=True, blank=True)
    selected_store = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Product(models.Model):
    name = models.TextField()
    brand = models.TextField()
    collection = models.TextField()
    relesed_date = models.DateField()
    image_url = models.TextField()
    price = models.IntegerField()
    description_url = models.TextField()
    wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Draw(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    url = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    reservation = models.ManyToManyField(settings.AUTH_USER_MODEL)