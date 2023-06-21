# Desafio

Crear una aplicacion web que sea de tipo single web page ([SPA](https://es.wikipedia.org/wiki/Single-page_application))


La aplicacion debe ser un [CRUD](https://es.wikipedia.org/wiki/CRUD) sobre un modelo Product

# Stack

* Python (3.8+)
* Django
* Javascript
* Bootstrapt (4.1+)
* sweetalert2
* **EN EL FRONT-END: Si conoce otra libreria o herramienta que le ayudara a realizar el challenge es libre de utilizarla**

# Consideraciones DJANGO

  * No utilizar django admin para generar las vistas
  * No utilizar django forms para generar los formularios
     * Los mismo deben ser generados en HTML con el formato de bootstrap

# Validaciones

 * No puede existir productos con la misma descripcion
 * No puede existir productos con el mismo codigo interno, ni con el mismo EAN (Codigo de barras)
 * El nombre del producto no puede superar los 90 caracteres
 * El codigo interno del producto debe ser de tipo entero e unico
 * Desde el formulario del producto debe ser posible crear una nueva marca
 * Se debe poder cargar precios al producto despues de que sean creados
 * Desde el listado de productos debe existir un boton por cada fila que muestre los precios de los productos como un detalle de la fila.
 * Los mensajes de las validaciones deben ser mostrados al usuario en un formato simple y entendible
 * Cuando se crea un producto nuevo, se debe enviar un correo a pjmakey2@gmail.com con la informacion del producto. La informacion debe ser visualizada en una tabla html

# Modelo de Product y Brand  
 La app debe basarse en los siguientes modelos de datos

```
class Brand(models.Model):
    brand = models.CharField()

class Product(models.Model):
    codigo_interno = models.IntegerField()
    ean = models.CharField()
    descripcion = models.CharField()
    brandobj = models.ForeignKey('Brand')

class Precios(models.Model):
    productobj = models.ForeignKey('Product')
    precio = models.FloatField()
    vigencia = models.DateField()

```

