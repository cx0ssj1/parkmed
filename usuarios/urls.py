from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path("registro/", views.registro, name="registro"),
    path("login/", views.login_paciente, name="login"),
    path("logout/", views.logout_paciente, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
