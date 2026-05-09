from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from estacionamientos.models import RegistroEstacionamiento
from .forms import LoginPoliciaForm
from .models import Policia

def es_policia(user):
    return user.is_authenticated and hasattr(user, "policia")

def login_policia(request):
    if request.user.is_authenticated and hasattr(request.user, "policia"):
        return redirect("policias:dashboard")

    if request.method == "POST":
        form = LoginPoliciaForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data["rut"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=rut, password=password)
            if user is not None and hasattr(user, "policia"):
                login(request, user)
                messages.success(
                    request,
                    f"Bienvenido, {user.get_full_name() or user.username}."
                )
                return redirect("policias:dashboard")
            messages.error(request, "Credenciales inválidas o sin permisos de policía.")
    else:
        form = LoginPoliciaForm()

    return render(request, "policias/login.html", {"form": form})

def logout_policia(request):
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect("core:login")

@login_required
@user_passes_test(es_policia, login_url="policias:login")
def dashboard(request):
    patente_buscada = request.GET.get("patente", "").strip().upper()
    resultados = []

    if patente_buscada:
        registros = RegistroEstacionamiento.objects.filter(
            patente__iexact=patente_buscada
        )
        for r in registros:
            estado = r.estado_actual()
            if estado in (
                RegistroEstacionamiento.ESTADO_EN_PROCESO,
                RegistroEstacionamiento.ESTADO_EN_URGENCIA,
            ):
                resultados.append(r)

    return render(request, "policias/dashboard.html", {
        "patente_buscada": patente_buscada,
        "resultados": resultados,
    })

@login_required
@user_passes_test(es_policia, login_url="policias:login")
def detalle(request, pk):
    registro = get_object_or_404(RegistroEstacionamiento, pk=pk)
    return render(request, "policias/detail.html", {"registro": registro})
