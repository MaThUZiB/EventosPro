from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.colors import black, HexColor

# Create your views here.
@login_required
def mis_compras(request):
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'compra/mis_compras.html', {'compras': compras})

@login_required
def detalle_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)
    asientos = compra.asientos_nombres.split(",") if compra.asientos_nombres else []
    evento = compra.evento_id  # ya es una instancia de Evento o None si fue null
    # Acceder a la ubicación desde el evento
    ubicacion = evento.ubicacion if evento else None
    return render(request, "compra/detalle_compra.html", {
        "ubicacion": ubicacion,
        "evento": evento,
        "compra": compra,
        "asientos": [a.strip() for a in asientos],  # quitamos espacios extra
    })

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black, HexColor
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def descargar_entrada(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id, usuario=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="entrada_{compra.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # ======= ESTILO GENERAL =======
    margen_x = 70
    y = height - 80

    # Encabezado
    p.setFont("Helvetica-Bold", 22)
    p.setFillColor(HexColor("#2c3e50"))
    p.drawCentredString(width / 2, y, "🎟 Entrada de Evento")

    # Línea decorativa
    y -= 20
    p.setStrokeColor(HexColor("#2c3e50"))
    p.setLineWidth(2)
    p.line(margen_x, y, width - margen_x, y)

    # ======= DATOS COMPRA =======
    y -= 40
    p.setFillColor(black)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(margen_x, y, "Datos de la compra:")

    p.setFont("Helvetica", 12)
    y -= 25
    p.drawString(margen_x, y, f"ID de compra: {compra.id}")
    y -= 18
    p.drawString(margen_x, y, f"Estado: {compra.estado}")
    y -= 18

    evento = compra.detalles.first().asiento.evento
    p.drawString(margen_x, y, f"Evento: {evento.nombre}")
    y -= 18
    p.drawString(margen_x, y, f"Total pagado: ${compra.total}")

    # ======= DATOS USUARIO =======
    y -= 35
    p.setFont("Helvetica-Bold", 14)
    p.drawString(margen_x, y, "Datos del comprador:")

    y -= 25
    p.setFont("Helvetica", 12)
    p.drawString(margen_x, y, f"Usuario: {request.user.username}")
    y -= 18
    p.drawString(margen_x, y, f"Email: {request.user.email}")
    y -= 18
    p.drawString(margen_x, y, f"RUT: {request.user.rut}")

    # ======= ASIENTOS =======
    y -= 35
    p.setFont("Helvetica-Bold", 14)
    p.drawString(margen_x, y, "Asientos:")

    y -= 20
    p.setFont("Helvetica", 12)

    for detalle in compra.detalles.all():
        p.drawString(margen_x + 20, y, f"• {detalle.nombre_asiento}")
        y -= 15
        if y < 80:  # salto de página automático
            p.showPage()
            y = height - 80

    # ======= MÉTODO DE PAGO =======
    y -= 30
    p.setFont("Helvetica-Oblique", 12)
    p.drawString(margen_x, y, f"Método de pago: {compra.pago.metodo}")

    # ======= FINAL =======
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


def cancelar_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    compra.cancelar()  # 👉 llama a tu método personalizado
    messages.success(request, "La compra fue cancelada correctamente.")
    return redirect("compra:mis_compras")