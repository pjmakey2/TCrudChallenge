# Create your views here.
# views.py

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from product.models import Product, Brand, Precios

#def product_list(request):
#    products = Product.objects.all()
#    brands = Brand.objects.all()
#    return render(request, 'product_list.html', {'products': products, 'brands': brands, 'product': products.first()})

def product_list(request):
    products = Product.objects.all()
    brands = Brand.objects.all()
    product_id = request.GET.get('product_id')  # Obtener el ID del producto desde la solicitud

    if product_id:
        product = products.filter(id=product_id).first()
    else:
        product = products.first()

    return render(request, 'product_list.html', {'products': products, 'brands': brands, 'product': product})


def product_create(request):
    error_message = ''
    if request.method == 'POST':
        codigo_interno = int(request.POST['codigo_interno'])
        ean = request.POST['ean']
        descripcion = request.POST['descripcion']
        brand_id = int(request.POST['brand'])
        
        # Validaciones
        if Product.objects.filter(descripcion=descripcion).exists():
            error_message = 'Ya existe un producto con esta descripción.'
        elif Product.objects.filter(codigo_interno=codigo_interno).exists():
            error_message = 'Ya existe un producto con este código interno.'
        elif Product.objects.filter(ean=ean).exists():
            error_message = 'Ya existe un producto con este código de barras (EAN).'
        elif len(descripcion) > 90:
            error_message = 'El nombre del producto no puede superar los 90 caracteres.'
        elif not Brand.objects.filter(id=brand_id).exists():
            error_message = 'La marca seleccionada no es válida.'
        
        if not error_message:
            brandobj = Brand.objects.get(id=brand_id)
            product = Product.objects.create(codigo_interno=codigo_interno, ean=ean, descripcion=descripcion, brandobj=brandobj)
            send_product_email(product)
            return redirect('product_list')
    
    brands = Brand.objects.all()
    return render(request, 'product_create.html', {'brands': brands, 'error_message': error_message})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    precios = Precios.objects.filter(productobj=product)
    return render(request, 'product_list.html', {'product': product, 'precios': precios})

def product_update(request, pk):
    error_message = ''
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        codigo_interno = int(request.POST['codigo_interno'])
        ean = request.POST['ean']
        descripcion = request.POST['descripcion']
        brand_id = int(request.POST['brand'])
        
        # Validaciones
        if Product.objects.filter(descripcion=descripcion).exclude(pk=pk).exists():
            error_message = 'Ya existe un producto con esta descripción.'
        elif Product.objects.filter(codigo_interno=codigo_interno).exclude(pk=pk).exists():
            error_message = 'Ya existe un producto con este código interno.'
        elif Product.objects.filter(ean=ean).exclude(pk=pk).exists():
            error_message = 'Ya existe un producto con este código de barras (EAN).'
        elif len(descripcion) > 90:
            error_message = 'El nombre del producto no puede superar los 90 caracteres.'
        elif not Brand.objects.filter(id=brand_id).exists():
            error_message = 'La marca seleccionada no es válida.'
        
        if not error_message:
            brandobj = Brand.objects.get(id=brand_id)
            product.codigo_interno = codigo_interno
            product.ean = ean
            product.descripcion = descripcion
            product.brandobj = brandobj
            product.save()
            return redirect('product_list')
    
    brands = Brand.objects.all()
    return render(request, 'product_update.html', {'product': product, 'brands': brands, 'error_message': error_message})

def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product_delete.html', {'product': product})

def brand_create(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand')
        Brand.objects.create(brand=brand_name)
        return redirect('product_list')
    return render(request, 'product_list.html')

def add_price(request, pk):
    product = Product.objects.get(id=pk)
    
    if request.method == 'POST':
        precio = request.POST.get('precio')
        vigencia = request.POST.get('vigencia')

        # Crear un nuevo objeto de Precios para el producto
        nuevo_precio = Precios(productobj=product, precio=precio, vigencia=vigencia)
        nuevo_precio.save()

        # Realizar otras acciones necesarias después de guardar el precio

        # Redirigir a la página de detalle del producto o a donde desees, {'product': Product.objects.all()}
        return redirect('product_detail', pk=product.id)
    else:
        return render(request, 'product_list.html')

def send_product_email(product):
    email_message = '''
    <h1>Información del producto</h1>
    <table style="border-collapse: collapse; width: 100%;">
        <tr>
            <th style="border: 1px solid black; padding: 8px; width: auto;">Código Interno</th>
            <th style="border: 1px solid black; padding: 8px; width: auto;">EAN</th>
            <th style="border: 1px solid black; padding: 8px; width: auto;">Descripción</th>
            <th style="border: 1px solid black; padding: 8px; width: auto;">Marca</th>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 8px; width: auto;">{}</td>
            <td style="border: 1px solid black; padding: 8px; width: auto;">{}</td>
            <td style="border: 1px solid black; padding: 8px; width: auto;">{}</td>
            <td style="border: 1px solid black; padding: 8px; width: auto;">{}</td>
        </tr>
    </table>
    '''.format(product.codigo_interno, product.ean, product.descripcion, product.brandobj.brand)
    send_mail('Nuevo producto creado', '', 'viictori19.vc@gmail.com', ['pjmakey2@gmail.com'], html_message=email_message)
