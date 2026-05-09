
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegistroPacienteForm, LoginPacienteForm
from .models import Paciente

def registro(request):
    if request.user.is_authenticated:
        return redirect('usuarios:dashboard')
    if request.method == 'POST':
        form = RegistroPacienteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['rut'],
                email=data['email'],
                password=data['password'],
                first_name=data['nombre_completo'],
            )
            Paciente.objects.create(
                user=user,
                rut=data['rut'],
                celular=data['celular']
            )
            messages.success(request, "Cuenta creada correctamente. Ahora puedes iniciar sesión.")
            return redirect('usuarios:login')
    else:
        form = RegistroPacienteForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def login_paciente(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "paciente"):
            return redirect("usuarios:dashboard")
        if hasattr(request.user, "policia"):
            return redirect("policias:dashboard")
        return redirect("core:index")
    
    if request.method == 'POST':
        form = LoginPacienteForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data['rut']
            password = form.cleaned_data['password']
            user = authenticate(request, username=rut, password=password)
            if user is None:
                messages.error(request, "RUT o contraseña incorrectos.")
            elif not hasattr(user, "paciente"):
                messages.error(
                    request,
                    "Esta cuenta no corresponde a un paciente. "
                    "Si eres policía, ingresa por el acceso correspondiente."
                )
            else:
                login(request, user)
                messages.success(request, f"Bienvenido, {user.first_name}.")
                return redirect("usuarios:dashboard")
    else:
        form = LoginPacienteForm()
    return render(request, 'usuarios/login.html', {'form': form})
def logout_paciente(request):
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect('usuarios:index')

@login_required
def dashboard(request):
    registros = request.user.estacionamientos.all()
    activos_o_proximos = [
        r for r in registros
        if r.estado_actual() != r.ESTADO_FINALIZADO
    ]
    historial = [
        r for r in registros
        if r.estado_actual() == r.ESTADO_FINALIZADO
    ]

    return render(request, "usuarios/dashboard.html", {
        "activos": activos_o_proximos,
        "historial": historial,
    })

def logout_paciente(request):
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect('core:index')