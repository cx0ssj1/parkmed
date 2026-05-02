from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RegistroEstacionamiento
from .forms import RegistroEstacionamientoForm

@login_required
def create(request):
    if request.method == "POST":
        form = RegistroEstacionamientoForm(request.POST, request.FILES)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.usuario = request.user
            registro.save()
            messages.success(request, "Estacionamiento registrado. ¡Ya estás protegido!")
            return redirect("usuarios:dashboard")
    else:
        form = RegistroEstacionamientoForm()
    return render(request, "estacionamientos/create.html", {"form": form})

@login_required
def eliminar(request, pk):
    registro = get_object_or_404(RegistroEstacionamiento, pk=pk, usuario=request.user)
    if request.method == "POST":
        registro.delete()
        messages.info(request, "Registro eliminado.")
    return redirect("usuarios:dashboard")