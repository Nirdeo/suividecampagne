from django.shortcuts import render

from . import messages, view_signin_signup_reset


def home(request):
    # Contexte générique
    context = context_processor(request)
    # Si utilisateur connecté
    if context["iduser"] != "":
        response = render(request, "home.html", context)
    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_connect}
        response = view_signin_signup_reset.login_view(request, context)
    return response


def context_processor(request):
    # Récupération des données du cookie pour alimenter le contexte générique
    context = {
        "iduser": request.COOKIES.get("iduser"),
        "nom": request.COOKIES.get("nom"),
        "prenom": request.COOKIES.get("prenom"),
        "email": request.COOKIES.get("email")
    }
    return context
