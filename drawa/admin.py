from django.contrib import admin
from .models import Store, Product, Draw

# Register your models here.
admin.site.register([Store, Product, Draw])