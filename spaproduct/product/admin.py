from django.contrib import admin

# Register your models here.
from .models import Precios, Brand, Product

admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Precios)