from django.shortcuts import render

from . import messages, view_signin_signup_reset


def context_processor(request):
    # Récupération des données du cookie pour alimenter le contexte générique
    context = {
        "isadmin": request.COOKIES.get("isadmin"),
        "iduser": request.COOKIES.get("iduser"),
        "nom": request.COOKIES.get("nom"),
        "prenom": request.COOKIES.get("prenom"),
        "email": request.COOKIES.get("email")
    }
    return context
