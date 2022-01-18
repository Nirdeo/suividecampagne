from django.urls import path
from suivi_de_campagne import views

urlpatterns = [
    path("", views.index, name="index"),
]