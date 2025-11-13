from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse

# Create your views here.
@login_required
def mis_compras(request):
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'compra/mis_compras.html', {'compras': compras})

@login_required
def detalle_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)
    asientos = compra.asientos_nombres.split(",") if compra.asientos_nombres else []
    
    return render(request, "compra/detalle_compra.html", {
        "compra": compra,
        "asientos": [a.strip() for a in asientos],  # quitamos espacios extra
    })

def descargar_entrada(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="entrada_{compra.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, height - 80, "Entrada para evento")
    p.setFont("Helvetica", 12)
    y = height - 130
    p.drawString(80, y, f"Compra ID: {compra.id}")
    y -= 20
    p.drawString(80, y, f"Evento: {compra.detalles.first().asiento.evento.nombre}")
    y -= 20
    p.drawString(80, y, f"Total pagado: ${compra.total}")
    y -= 20
    p.drawString(80, y, f"Email comprador: {request.user.username}")
    y -= 30
    p.drawString(80, y, f"Rut comprador: {request.user.rut}")
    y -= 30
    p.drawString(80, y, f"Email comprador: {request.user.email}")
    y -= 30

    p.setFont("Helvetica-Bold", 13)
    p.drawString(80, y, "Asientos:")
    y -= 20
    p.setFont("Helvetica", 12)
    for detalle in compra.detalles.all():
        p.drawString(100, y, f"• {detalle.nombre_asiento}")
        y -= 18

    y -= 20
    p.setFont("Helvetica-Oblique", 11)
    p.drawString(80, y, f"Método de pago: {compra.pago.metodo}")

    # Finalizar
    p.showPage()
    p.save()

    return response

@login_required
def confirmar_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)
    pago = get_object_or_404(Pago, compra=compra)

    if request.method == "POST":
        metodo = request.POST.get("metodo") 
        if metodo not in ["WebPay", "Transferencia", "PayPal"]:
            messages.error(request, "Método de pago no válido.")
            return redirect('compra:confirmar_compra', compra_id=compra.id)

        pago.metodo = metodo
        pago.save()

        return redirect('compra:procesar_pago', compra_id=compra.id)

    detalles = compra.detalles.all()
    return render(request, 'compra/confirmar_compra.html', {
        'compra': compra,
        'pago': pago,
        'detalles': detalles
    })

@login_required
def procesar_pago(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)
    pago = get_object_or_404(Pago, compra=compra)

    if request.method == "POST":
        # Simulación: aprobamos el pago
        pago.estado = 'aprobado'
        pago.save()
        messages.success(request, f"Pago por {pago.metodo} realizado correctamente 🎉")
        return redirect('compra:confirmacion_compra', compra_id=compra.id)

    return render(request, 'compra/procesar_pago.html', {
        'compra': compra,
        'pago': pago,
    })

@login_required
def confirmacion_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)
    return render(request, "compra/confirmacion_compra.html", {"compra": compra})
