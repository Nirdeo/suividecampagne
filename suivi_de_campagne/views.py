from django.shortcuts import render


def home(request):
    return render(request, 'home.html')


def context_processor(request):
    return {
        "base": request.COOKIES.get("base"),
        "nom_contact": request.COOKIES.get("nom_contact"),
        "prenom": request.COOKIES.get("prenom"),
        "fonction": request.COOKIES.get("fonction"),
        "email": request.COOKIES.get("email"),
        "telephone": request.COOKIES.get("telephone"),
        "skype": request.COOKIES.get("skype"),
        "categories": request.COOKIES.get("categories"),
        "siret": request.COOKIES.get("siret"),
        "nom_partenaire": request.COOKIES.get("nom_partenaire"),
    }
