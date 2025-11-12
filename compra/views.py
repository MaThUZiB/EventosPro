from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
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
