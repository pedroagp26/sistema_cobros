from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Servicio

# 1. LISTA DE CLIENTES
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'gestion/lista_clientes.html', {'clientes': clientes})

# 2. DETALLE / FICHA DEL CLIENTE
def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    return render(request, 'gestion/detalle_cliente.html', {'cliente': cliente})

# 3. AGREGAR NUEVO SERVICIO
def agregar_servicio(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    if request.method == "POST":
        tipo = request.POST.get('tipo_servicio')
        empresa = request.POST.get('empresa')
        num = request.POST.get('num_servicio')
        obs = request.POST.get('observaciones')
        
        Servicio.objects.create(
            cliente=cliente,
            tipo_servicio=tipo,
            empresa=empresa,
            num_servicio=num,
            observaciones=obs
        )
        return redirect('detalle_cliente', cliente_id=cliente.id)
        
    return render(request, 'gestion/agregar_servicio.html', {'cliente': cliente})

# 4. EDITAR DATOS DEL CLIENTE (¡Esta es la que faltaba!)
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    if request.method == "POST":
        cliente.nombre_completo = request.POST.get('nombre')
        cliente.ci = request.POST.get('ci')
        cliente.celular = request.POST.get('celular')
        cliente.save()
        return redirect('lista_clientes')
        
    return render(request, 'gestion/editar_cliente.html', {'cliente': cliente})

def editar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    cliente_id = servicio.cliente.id # Guardamos el ID para volver a su ficha
    
    if request.method == "POST":
        servicio.tipo_servicio = request.POST.get('tipo_servicio')
        servicio.empresa = request.POST.get('empresa')
        servicio.num_servicio = request.POST.get('num_servicio')
        servicio.observaciones = request.POST.get('observaciones')
        servicio.save()
        return redirect('detalle_cliente', cliente_id=cliente_id)
        
    return render(request, 'gestion/editar_servicio.html', {'servicio': servicio})

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def generar_pdf_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    
    # Crear el objeto de respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Ficha_{cliente.ci}.pdf"'

    # Crear el lienzo (canvas)
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # --- ENCABEZADO ---
    p.setFillColor(colors.HexColor("#1a237e"))
    p.rect(0, height - 80, width, 80, fill=True, stroke=False)
    
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, "FICHA TÉCNICA DE CLIENTE")
    
    # --- DATOS DEL CLIENTE ---
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 120, f"Nombre: {cliente.nombre_completo}")
    p.drawString(50, height - 140, f"CI: {cliente.ci}")
    p.drawString(50, height - 160, f"Celular: {cliente.celular or 'N/A'}")
    
    p.line(50, height - 180, width - 50, height - 180)

    # --- SERVICIOS ---
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 210, "SERVICIOS REGISTRADOS")
    
    y = height - 240
    p.setFont("Helvetica", 11)
    
    for servicio in cliente.servicios.all():
        if y < 100: # Si se acaba la hoja, crear una nueva
            p.showPage()
            y = height - 50
            
        p.setFillColor(colors.HexColor("#f0f0f0"))
        p.rect(50, y - 45, width - 100, 50, fill=True, stroke=False)
        
        p.setFillColor(colors.black)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(60, y - 15, f"{servicio.empresa} ({servicio.get_tipo_servicio_display()})")
        
        p.setFont("Courier-Bold", 13)
        p.setFillColor(colors.red)
        p.drawString(60, y - 35, f"CUENTA: {servicio.num_servicio}")
        
        y -= 65 # Espacio entre servicios

    p.showPage()
    p.save()
    return response