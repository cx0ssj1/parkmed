from django.shortcuts import render
from estacionamientos.models import RegistroEstacionamiento

def index(request):
    todos = RegistroEstacionamiento.objects.exclude(
        estado=RegistroEstacionamiento.ESTADO_FINALIZADO
    )

    activos_publicos = []
    for r in todos:
        estado = r.estado_actual()
        if estado in (
            RegistroEstacionamiento.ESTADO_EN_PROCESO,
            RegistroEstacionamiento.ESTADO_EN_URGENCIA,
        ):
            activos_publicos.append(r)

    return render(request, "core/index.html", {
        "estacionamientos": activos_publicos,
        "total": len(activos_publicos),
    })


def about(request):
    return render(request, 'core/about.html') 