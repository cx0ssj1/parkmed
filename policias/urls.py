from django.urls import path
from . import views

app_name = "policias"

urlpatterns = [
    path("login/", views.login_policia, name="login"),
    path("logout/", views.logout_policia, name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("detail/<int:pk>/", views.detalle, name="detail"),
]