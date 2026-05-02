from django.urls import path
from . import views

app_name = 'estacionamientos'

urlpatterns = [
    path("create/", views.create, name="create"),
    path("<int:pk>/eliminar/", views.eliminar, name="eliminar"),
]