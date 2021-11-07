from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import CharField


# class User(AbstractUser):
#     phone = models.TextField()


class Store(models.Model):
    name = CharField(max_length=50, null=True, default=' ')
    # is_online = models.BooleanField()
    nation = models.TextField(null=True, blank=True)
    # location_si = models.TextField(null=True, blank=True)
    # location_gu = models.TextField(null=True, blank=True)
    # location_dong = models.TextField(null=True, blank=True)
    # location_detail = models.TextField(null=True, blank=True)
    # tel = models.TextField(null=True, blank=True)
    
    instagram_url = models.TextField(null=True, blank=True, default='')
    kakao_url = models.TextField(null=True, blank=True, default='')
    nation_flag_url = models.TextField()
    store_img_url = models.TextField(null=True)
    select = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='selected_stores',
        blank=True)


class Product(models.Model):
    name_kor = models.TextField()
    name_eng = models.TextField()
    brand = models.TextField()
    collection = models.TextField()
    code = models.CharField(max_length=50)
    relesed_date = models.DateField()
    image_url = models.TextField()
    price = models.IntegerField()

    # description_url = models.TextField()
    view_count = models.IntegerField(default=0)
    wish = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='wishlist', 
        blank=True)


class Draw(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    url = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    can_delivery = models.BooleanField(default=True)
    is_direct = models.BooleanField(default=True)
    reserve = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='reserved_draws',
        blank=True)
    participate = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='participated_draws', 
        blank=True
    )