import datetime

from bson import ObjectId
from django.contrib.auth import logout
from django.shortcuts import render, redirect

from suivi_de_campagne import forms, emails, messages
from utils import database, functions


def logout_user(request):
    logout(request)
    return redirect('login')


def login_view(request):
    form = forms.LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            # Récupération des infos
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            # Connexion à la bdd
            database.mongodb.openConnection()
            if database.mongodb.isAlive():
                # récupération de l'utilisateur dans mongo avec un find
                predicate = {"email": username,
                             "password": functions.hasher(password)}
                projection = {"_id": 1, "email": 1, "password": 1}
                user = database.mongodb.suivicampagne.utilisateurs.find_one(
                    predicate, projection)
                # Vérif user
                if user is not None:
                    response = render(request, "home.html")
                else:
                    context = {"msg": "Invalid credentials"}
                    response = render(request, "login.html", context)
            else:
                context = {
                    "msg": "La base de donnée est déconnectée actuellement"}
                response = render(request, "login.html", context)
        else:
            context = {"msg": "Error validating the form"}
            response = render(request, "login.html", context)
    else:
        response = render(request, "login.html", {"form": form})

    return response


def forgot_password(request):
    context = {}
    return render(request, "forgot_password.html", context)


def reset_password(request):
    if request.method == "POST":
        form = forms.formulaire_reset_password(request.POST)
        if form.is_valid():
            # Récupération des données du formulaire
            username = form.cleaned_data["email"]

            # Ouverture de la connexion à la base de données
            database.mongodb.openConnection()

            if database.mongodb.isAlive():
                # Recherche de l'utilisateur en base
                predicate = {"email": username}
                projection = {"_id": 1, "businessunit": 1,
                              "nom": 1, "prenom": 1, "email": 1, }
                user = database.mongodb.suivicampagne.utilisateurs.find_one(
                    predicate, projection)

                # Si l'utilisateur existe bien
                if user is not None:

                    # Génération du mot de passe et tracking
                    mot_de_passe = functions.generate_password()
                    functions.mark(
                        " * Nouveau mot de passe généré pour {0} : {1}".format(username, mot_de_passe))

                    # Modification effective
                    filter = {"_id": user["_id"]}
                    update = {
                        "$set": {
                            "password": functions.hasher(mot_de_passe),
                            "idmodification": user["_id"],
                            "datemodification": datetime.datetime.now()
                        }
                    }
                    database.mongodb.suivicampagne.utilisateurs.update_one(
                        filter, update)

                    # Envoi du mot de passe modifié par e-mail
                    contenu = emails.reset_password.format(mot_de_passe)
                    functions.send_email(
                        username, "suivicampagne - nouveau mot de passe", contenu)

                    # Valeur de retour
                    functions.tracking(
                        "Demande réinitialisation mot de passe", ObjectId(user["_id"]))
                    context = {
                        "message": messages.reset_password + user["email"]}
                else:
                    # Retour sur la fenêtre de connexion avec erreur
                    context = {"erreur": messages.error_user}
            else:
                # Retour sur la fenêtre de connexion avec erreur
                context = {"erreur": messages.error_database}
            response = render(request, "login.html", context)
    return response
