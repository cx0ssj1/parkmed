from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from usuarios.views import registro
from .models import RegistroEstacionamiento
from .forms import RegistroEstacionamientoForm, EditarRegistroForm


@login_required
def create(request):
    if request.method == "POST":
        form = RegistroEstacionamientoForm(request.POST, request.FILES)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.paciente = request.user.paciente
            registro.save()
            messages.success(request, "Estacionamiento registrado. ¡Ya estás protegido!")
            return redirect("usuarios:dashboard")
    else:
        form = RegistroEstacionamientoForm()
    return render(request, "estacionamientos/create.html", {"form": form})

@login_required
def eliminar(request, pk):
    registro = get_object_or_404(
        RegistroEstacionamiento,
        pk=pk,
        paciente=request.user.paciente  
    )
    if request.method == "POST":
        registro.delete()
        messages.info(request, "Registro eliminado.")
    return redirect("usuarios:dashboard")



@login_required
def editar(request, pk):
    registro = get_object_or_404(
        RegistroEstacionamiento,
        pk=pk,
        paciente=request.user.paciente  
    )

    if not registro.es_editable():
        messages.error(
            request,
            "Este registro ya finalizó y no se puede editar."
        )
        return redirect("usuarios:dashboard")
    
    if request.method == "POST":
        form = EditarRegistroForm(request.POST, request.FILES, instance=registro)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro actualizado correctamente.")
            return redirect("usuarios:dashboard")
    else:
        form = EditarRegistroForm(instance=registro)

    return render(request, "estacionamientos/editar.html", {
        "form": form,
        "registro": registro,
    })