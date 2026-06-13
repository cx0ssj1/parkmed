from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from usuarios.models import Paciente
from policias.models import Policia
from .forms import CrearUsuarioForm, EditarUsuarioForm

def es_admin(user):
    return user.is_authenticated and user.is_superuser


def login_admin(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("administracion:lista_usuarios")
        return redirect("core:index")

    if request.method == "POST":
        rut = request.POST.get("rut", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=rut, password=password)

        if user is None:
            messages.error(request, "RUT o contraseña incorrectos.")
        elif not user.is_superuser:
            messages.error(
                request,
                "Esta cuenta no tiene permisos de administrador."
            )
        else:
            login(request, user)
            messages.success(request, f"Bienvenido, {user.get_full_name() or user.username}.")
            return redirect("administracion:lista_usuarios")

    return render(request, "administracion/login.html")


def logout_admin(request):
    logout(request)
    messages.info(request, "Sesión cerrada.")
    return redirect("core:index")

@user_passes_test(es_admin, login_url="administracion:login")
def lista_usuarios(request):
    usuarios = User.objects.all().order_by("username")

    datos = []
    for u in usuarios:
        if hasattr(u, "policia"):
            rol = f"Policía ({u.policia.get_institucion_display()})"
        elif hasattr(u, "paciente"):
            rol = "Paciente"
        elif u.is_superuser:
            rol = "Administrador"
        else:
            rol = "Sin rol"
        datos.append({"usuario": u, "rol": rol})

    return render(request, "administracion/lista_usuarios.html", {
        "datos": datos,
    })

@user_passes_test(es_admin, login_url="administracion:login")
def crear_usuario(request):
    if request.method == "POST":
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data["rut"],
                email=data["email"],
                password=data["password"],  
                first_name=data["nombre_completo"],
            )

            if data["rol"] == CrearUsuarioForm.ROL_PACIENTE:
                Paciente.objects.create(
                    user=user,
                    rut=data["rut"],
                    celular=data["celular"],
                )
            else:
                Policia.objects.create(
                    user=user,
                    rut=data["rut"],
                    institucion=data["institucion"],
                    numero_placa=data["numero_placa"] or None,
                )

            messages.success(
                request,
                f"Usuario {data['nombre_completo']} creado correctamente."
            )
            return redirect("administracion:lista_usuarios")
    else:
        form = CrearUsuarioForm()

    return render(request, "administracion/crear_usuario.html", {"form": form})

@user_passes_test(es_admin, login_url="administracion:login")
def editar_usuario(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = EditarUsuarioForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            user.first_name = data["nombre_completo"]
            user.email = data["email"]
            if data["password"]:
                user.set_password(data["password"])  
            user.save()

            if hasattr(user, "paciente"):
                user.paciente.celular = data["celular"]
                user.paciente.save()
            elif hasattr(user, "policia"):
                user.policia.institucion = data["institucion"]
                user.policia.numero_placa = data["numero_placa"] or None
                user.policia.save()

            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("administracion:lista_usuarios")
    else:
        inicial = {
            "nombre_completo": user.first_name,
            "email": user.email,
        }
        if hasattr(user, "paciente"):
            inicial["celular"] = user.paciente.celular
        elif hasattr(user, "policia"):
            inicial["institucion"] = user.policia.institucion
            inicial["numero_placa"] = user.policia.numero_placa
        form = EditarUsuarioForm(initial=inicial)

    return render(request, "administracion/editar_usuario.html", {
        "form": form,
        "usuario": user,
    })

@user_passes_test(es_admin, login_url="administracion:login")
def eliminar_usuario(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user == request.user:
        messages.error(request, "No puedes eliminar tu propia cuenta.")
        return redirect("administracion:lista_usuarios")

    if user.is_superuser:
        messages.error(request, "No se puede eliminar una cuenta de administrador.")
        return redirect("administracion:lista_usuarios")

    if request.method == "POST":
        nombre = user.first_name or user.username
        user.delete()  
        messages.info(request, f"Usuario {nombre} eliminado.")

    return redirect("administracion:lista_usuarios")