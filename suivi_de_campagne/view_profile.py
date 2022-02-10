from datetime import datetime

from bson import ObjectId
from django.contrib import messages as msg
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from suivi_de_campagne import view_signin_signup_reset
from utils import database
from utils.functions import hasher
from . import forms
from . import messages
from . import views


def profile_detail(request, identifier=None):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            context["identifier"] = identifier

            # Partenaire existant
            if identifier:
                user = database.mongodb.suivicampagne.utilisateurs.find_one({"_id": ObjectId(identifier)},
                                                                            {"_id": 1, "civilite": 1,
                                                                             "nom": 1, "prenom": 1, "description": 1,
                                                                             "email": 1})
                if user:
                    # Affichage de la page détails utilisateur
                    values = {}
                    for key, value in user.items():
                        values[key] = value
                    form = forms.UserForm(initial=values)
                    context["form"] = form
                    response = render(request, "profile_detail.html", context)
                else:
                    form = forms.UserForm()
                    context["erreur"] = messages.not_found
                    context["form"] = form
                    response = render(request, "profile_detail.html", context)
            else:
                form = forms.UserForm()
                context["form"] = form
                response = render(request, "profile_detail.html", context)
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        # Retour sur la mire de connexion
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)
    # Fin de fonction
    return response


def edit_profile(request, identifier):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            if request.method == "POST":
                # Validation du formulaire
                form = forms.UserForm(request.POST)
                if form.is_valid():
                    # Récupération des données
                    civilite = form.cleaned_data["civilite"]
                    name = form.cleaned_data["nom"]
                    firstname = form.cleaned_data["prenom"]
                    email = form.cleaned_data["email"]
                    password = form.cleaned_data["mot_de_passe"]
                    comments = form.cleaned_data["description"]

                    filter = {"_id": ObjectId(identifier)}
                    update = {
                        "$set": {
                            "civilite": civilite,
                            "nom": name,
                            "prenom": firstname,
                            "description": comments,
                            "email": email,
                            "datemodification": datetime.now()
                        }
                    }
                    # Si le mot de passe est mis à jour, on l'encrypte !
                    if password != "":
                        update["$set"]["password"] = hasher(password)
                        update["$set"]["security_check"] = datetime.now()

                    database.mongodb.suivicampagne.utilisateurs.update_one(
                        filter, update)

                    response = HttpResponseRedirect(
                        reverse("profile-detail", kwargs={"identifier": identifier}))
                    # Si les informations de l'utilisateur actif sont modifiées, MAJ des cookies
                    if identifier == context["iduser"]:
                        response.set_cookie("nom", name)
                        response.set_cookie("prenom", firstname)
                        response.set_cookie("email", email)
                else:
                    msg.add_message(request, msg.ERROR, form.errors)
                    response = HttpResponseRedirect(
                        reverse("profile-detail", kwargs={"identifier": identifier}))
            else:
                # Valeur de retour
                response = HttpResponseRedirect(
                    reverse("profile-detail", kwargs={"identifier": identifier}))
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        # Retour sur la mire de connexion
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)

    # Fin de fonction
    return response
