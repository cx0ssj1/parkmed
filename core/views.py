from django.shortcuts import render
from datetime import datetime, timedelta

def index(request):
    now = datetime.now()
    # datos de ejemplooo
    estacionamientos_activos = [
                {
            "patente": "JKLM23",
            "estado": "EN_PROCESO",
            "hora_salida": now + timedelta(hours=2, minutes=15),
            "tipo": "Estándar",
        },
        {
            "patente": "BCDF45",
            "estado": "EN_URGENCIA",
            "hora_salida": now + timedelta(hours=2, minutes=45),
            "tipo": "Movilidad reducida",
        },
        {
            "patente": "GHJK67",
            "estado": "EN_PROCESO",
            "hora_salida": now + timedelta(minutes=40),
            "tipo": "Estándar",
        },
        {
            "patente": "PQRS89",
            "estado": "EN_PROCESO",
            "hora_salida": now + timedelta(hours=1, minutes=30),
            "tipo": "Estándar",
        },
    ]
    contexto = {
        "estacionamientos": estacionamientos_activos,
        "total": len(estacionamientos_activos),
    }
    return render(request, 'core/index.html', contexto)

def about(request):
    return render(request, 'core/about.html') 