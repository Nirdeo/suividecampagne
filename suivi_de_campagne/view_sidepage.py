from datetime import datetime

from bson import ObjectId
from django.contrib import messages as msg
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from suivi_de_campagne import view_signin_signup_reset
from utils import database
from . import forms
from . import messages
from . import views


def view_sidepage(request):
    if database.mongodb.isAlive():
        # Affichage de la page principale
        form_theme = forms.ThemeForm(request.POST)
        form_blacklist_theme = forms.BlacklistThemeForm(request.POST)
        form_levier = forms.LevierForm(request.POST)
        form_modele_economique = forms.ModeleEconomiqueForm(request.POST)
        response = render(
            request, "sidepage_create.html",
            {"form_theme": form_theme, "form_blacklist_theme": form_blacklist_theme, "form_levier": form_levier,
             "form_modele_economique": form_modele_economique})
    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_database}
        response = view_signin_signup_reset.login_view(request, context)
    return response


def create_theme(request):
    if database.mongodb.isAlive():
        if request.method == "POST":
            # Validation du formulaire
            form_theme = forms.ThemeForm(request.POST)
            if form_theme.is_valid():
                # Contexte générique
                context = views.context_processor(request)

                # Récupération des données
                libelle_theme = form_theme.cleaned_data["libelle_theme"]

                # Création du thème
                theme = {
                    "libelle_theme": libelle_theme,
                    "date_creation": datetime.now(),
                }

                # Insertion des données dans la base de données
                identifier_theme = database.mongodb.suivicampagne.themes.insert_one(
                    theme).inserted_id
                identifier_theme = str(identifier_theme)

                # Valeur de retour
                response = HttpResponseRedirect(reverse("list-sidepage"))
            else:
                msg.add_message(request, msg.ERROR, form_theme.errors)
                response = HttpResponseRedirect(reverse("create-theme"))
        else:
            # Valeur de retour
            response = HttpResponseRedirect(reverse("create-theme"))
    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_database}
        response = view_signin_signup_reset.login_view(request, context)
    return response


def create_blacklist_theme(request):
    if database.mongodb.isAlive():
        if request.method == "POST":
            # Validation du formulaire
            form_blacklist_theme = forms.BlacklistThemeForm(request.POST)
            if form_blacklist_theme.is_valid():
                # Contexte générique
                context = views.context_processor(request)

                # Récupération des données
                libelle_blacklist_theme = form_blacklist_theme.cleaned_data[
                    "libelle_blacklist_theme"]

                # Création de la liste noire des themes
                blacklist_theme = {
                    "libelle_blacklist_theme": libelle_blacklist_theme,
                    "datecreation": datetime.now(),
                }

                # Insertion des données dans la base de données
                identifier_blacklist_theme = database.mongodb.suivicampagne.themes_liste_noire.insert_one(
                    blacklist_theme).inserted_id
                identifier_blacklist_theme = str(identifier_blacklist_theme)

                # Valeur de retour
                response = HttpResponseRedirect(reverse("list-sidepage"))
            else:
                msg.add_message(request, msg.ERROR,
                                form_blacklist_theme.errors)
                response = HttpResponseRedirect(
                    reverse("create-blacklist-theme"))
        else:
            # Valeur de retour
            response = HttpResponseRedirect(reverse("create-blacklist-theme"))
    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_database}
        response = view_signin_signup_reset.login_view(request, context)
    return response


def create_levier(request):
    if database.mongodb.isAlive():
        if request.method == "POST":
            # Validation du formulaire
            form_levier = forms.LevierForm(request.POST)
            if form_levier.is_valid():
                # Contexte générique
                context = views.context_processor(request)

                # Récupération des données
                libelle_levier = form_levier.cleaned_data["libelle_levier"]

                # Création du levier
                levier = {
                    "libelle_levier": libelle_levier,
                    "datecreation": datetime.now(),
                }

                # Insertion des données dans la base de données
                identifier_levier = database.mongodb.suivicampagne.leviers.insert_one(
                    levier).inserted_id
                identifier_levier = str(identifier_levier)

                # Valeur de retour
                response = HttpResponseRedirect(reverse("list-sidepage"))
            else:
                msg.add_message(request, msg.ERROR, form_levier.errors)
                response = HttpResponseRedirect(reverse("create-levier"))
        else:
            # Valeur de retour
            response = HttpResponseRedirect(reverse("create-levier"))
    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_database}
        response = view_signin_signup_reset.login_view(request, context)
    return response


def create_modele_economique(request):
    if database.mongodb.isAlive():
        if request.method == "POST":
            # Validation du formulaire
            form_modele_economique = forms.ModeleEconomiqueForm(request.POST)
            if form_modele_economique.is_valid():
                # Contexte générique
                context = views.context_processor(request)

                # Récupération des données
                libelle_modele_economique = form_modele_economique.cleaned_data[
                    "libelle_modele_economique"]

                # Création du modèle économique
                modele_economique = {
                    "libelle_modele_economique": libelle_modele_economique,
                    "datecreation": datetime.now(),
                }

                # Insertion des données dans la base de données
                identifier_modele_economique = database.mongodb.suivicampagne.modeles_economiques.insert_one(
                    modele_economique).inserted_id
                identifier_modele_economique = str(
                    identifier_modele_economique)

                # Valeur de retour
                response = HttpResponseRedirect(reverse("list-sidepage"))
            else:
                msg.add_message(request, msg.ERROR,
                                form_modele_economique.errors)
                response = HttpResponseRedirect(
                    reverse("create-modele-economique"))
        else:
            # Valeur de retour
            response = HttpResponseRedirect(
                reverse("create-modele-economique"))
    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_database}
        response = view_signin_signup_reset.login_view(request, context)
    return response


def delete_theme(request, identifier):
    if database.mongodb.isAlive():
        database.mongodb.suivicampagne.themes.delete_one(
            {"_id": ObjectId(identifier)})
        response = HttpResponseRedirect(reverse("list-sidepage"))
    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_database}
        response = view_signin_signup_reset.login_view(request, context)
    return response


def delete_blacklist_theme(request, identifier):
    if database.mongodb.isAlive():
        database.mongodb.suivicampagne.themes_liste_noire.delete_one(
            {"_id": ObjectId(identifier)})
        response = HttpResponseRedirect(reverse("list-sidepage"))
    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_database}
        response = view_signin_signup_reset.login_view(request, context)
    return response


def delete_levier(request, identifier):
    if database.mongodb.isAlive():
        database.mongodb.suivicampagne.leviers.delete_one(
            {"_id": ObjectId(identifier)})
        response = HttpResponseRedirect(reverse("list-sidepage"))
    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_database}
        response = view_signin_signup_reset.login_view(request, context)
    return response


def delete_modele_economique(request, identifier):
    if database.mongodb.isAlive():
        database.mongodb.suivicampagne.modeles_economiques.delete_one(
            {"_id": ObjectId(identifier)})
        response = HttpResponseRedirect(reverse("list-sidepage"))
    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_database}
        response = view_signin_signup_reset.login_view(request, context)
    return response


def list_sidepage(request):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        match = {"$match": {}}
        project = {"$project": {"libelle_theme": 1, "datecreation": 1}}
        sort = {"$sort": {"datecreation": 1}}
        themes_mongo = database.mongodb.suivicampagne.themes.aggregate(
            [match, project, sort])
        themes = []
        for theme in themes_mongo:
            theme["id"] = theme["_id"]
            themes.append(theme)
        context["themes"] = themes
        match = {"$match": {}}
        project = {"$project": {
            "libelle_blacklist_theme": 1, "datecreation": 1}}
        sort = {"$sort": {"datecreation": 1}}
        themes_liste_noire_mongo = database.mongodb.suivicampagne.themes_liste_noire.aggregate(
            [match, project, sort])
        themes_liste_noire = []
        for theme in themes_liste_noire_mongo:
            theme["id"] = theme["_id"]
            themes_liste_noire.append(theme)
        context["themes_liste_noire"] = themes_liste_noire
        match = {"$match": {}}
        project = {"$project": {"libelle_levier": 1, "datecreation": 1}}
        sort = {"$sort": {"datecreation": 1}}
        leviers_mongo = database.mongodb.suivicampagne.leviers.aggregate(
            [match, project, sort])
        leviers = []
        for levier in leviers_mongo:
            levier["id"] = levier["_id"]
            leviers.append(levier)
        context["leviers"] = leviers
        match = {"$match": {}}
        project = {"$project": {
            "libelle_modele_economique": 1, "datecreation": 1}}
        sort = {"$sort": {"datecreation": 1}}
        modeles_economiques_mongo = database.mongodb.suivicampagne.modeles_economiques.aggregate(
            [match, project, sort])
        modeles_economiques = []
        for modele_economique in modeles_economiques_mongo:
            modele_economique["id"] = modele_economique["_id"]
            modeles_economiques.append(modele_economique)
        context["modeles_economiques"] = modeles_economiques
        response = render(request, "sidepage_list.html", context)
    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_database}
        response = view_signin_signup_reset.login_view(request, context)
    return response
