from django.db import models

# Create your models here.
class Brand(models.Model):
    brand = models.CharField(max_length=255)

    def __str__(self):
        return self.brand

class Product(models.Model):
    codigo_interno = models.IntegerField(unique=True)
    ean = models.CharField(unique=True, max_length=255)
    descripcion = models.CharField(max_length=90)
    brandobj = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

class Precios(models.Model):
    productobj = models.ForeignKey(Product, on_delete=models.CASCADE)
    precio = models.FloatField()
    vigencia = models.DateField()

    def __str__(self):
        return f"{self.productobj.descripcion} - {self.precio}"
    