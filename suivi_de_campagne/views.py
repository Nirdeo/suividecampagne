from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def context_processor(request):
    # Récupération des données du cookie pour alimenter le contexte générique
    context = {
        "iduser" : request.COOKIES.get("iduser"),
        "nom" : request.COOKIES.get("nom"),
        "prenom" : request.COOKIES.get("prenom"),
        "email" : request.COOKIES.get("email")
    }
    return context
