from django.contrib import admin
from .models import Store, Product, Draw

from .models import Draw, Product

# Register your models here.
admin.site.register([Store, Product, Draw])

