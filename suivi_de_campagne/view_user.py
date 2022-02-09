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

def list_user(request):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "" :
            match = {"$match": {}}
            project = {"$project": {"nom": 1, "prenom": 1, "email" : 1, "datecreation": 1, "datemodification": 1}}
            sort = {"$sort": {"nom": 1}}
            users_mongo = database.mongodb.suivicampagne.utilisateurs.aggregate([match, project, sort])
            users = []
            for utilisateur in users_mongo:
                utilisateur["id"] = str(utilisateur["_id"])
                users.append(utilisateur)

            context["utilisateurs"] = users
            response =  render(request, "user_list.html", context)
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        # Retour sur la mire de connexion
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)
    return response

def user_detail(request, identifier=None):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "" :
            context["identifier"] = identifier

            # Partenaire existant
            if identifier :
                user = database.mongodb.suivicampagne.utilisateurs.find_one({"_id" : ObjectId(identifier)},{ "_id": 1, "admin": 1, "civilite" : 1, "nom": 1, "prenom": 1, "description": 1, "email": 1 })
                if user:
                    # Affichage de la page détails utilisateur
                    values = {}
                    for key, value in user.items() :
                        values[key] = value
                    form = forms.UserForm(initial=values)
                    context["form"] = form
                    response = render(request, "user_detail.html", context)
                else:
                    form = forms.UserForm()
                    context["erreur"] = messages.not_found
                    context["form"] = form
                    response = render(request, "user_detail.html", context)
            else :
                form = forms.UserForm()
                context["form"] = form
                response = render(request, "user_detail.html", context)
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

def create_user(request):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "" :
            if request.method == "POST":
                # Validation du formulaire
                form = forms.UserForm(request.POST)
                if form.is_valid():
                    # Récupération des données
                    admin = form.cleaned_data["admin"]
                    civilite = form.cleaned_data["civilite"]
                    name = form.cleaned_data["nom"]
                    firstname = form.cleaned_data["prenom"]
                    email = form.cleaned_data["email"]
                    comments = form.cleaned_data["description"]

                    record = {
                        "admin": admin,
                        "civilite": civilite,
                        "nom": name,
                        "prenom": firstname,
                        "description": comments,
                        "email": email,
                        "password" : hasher("defaultpwd"),
                        "security_check" : datetime.now(),
                        "datecreation": datetime.now(),
                        "datemodification": datetime.now()
                    }
                    identifier = database.mongodb.suivicampagne.utilisateurs.insert_one(
                        record).inserted_id
                    identifier = str(identifier)

                    # Valeur de retour
                    response = HttpResponseRedirect(reverse("user-detail", kwargs={"identifier" : identifier}))
                else:
                    msg.add_message(request, msg.ERROR, form.errors)
                    response = HttpResponseRedirect(reverse("user-detail"))
            else:
                # Valeur de retour
                response = HttpResponseRedirect(reverse("user-detail"))
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        # Retour sur la mire de connexion
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)

    return response

def edit_user(request, identifier):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "" :
            if request.method == "POST":
                # Validation du formulaire
                form = forms.UserForm(request.POST)
                if form.is_valid() :
                    # Récupération des données
                    admin = form.cleaned_data["admin"]
                    civilite = form.cleaned_data["civilite"]
                    name = form.cleaned_data["nom"]
                    firstname = form.cleaned_data["prenom"]
                    email = form.cleaned_data["email"]
                    password = form.cleaned_data["mot_de_passe"]
                    comments = form.cleaned_data["description"]

                    filter = { "_id" : ObjectId(identifier) }
                    update = { 
                        "$set" : {
                            "admin": admin,
                            "civilite": civilite,
                            "nom": name,
                            "prenom": firstname,
                            "description": comments,
                            "email": email,
                            "datemodification": datetime.now()
                        }
                    }
                    # Si le mot de passe est mis à jour, on l'encrypte !
                    if password != "" :
                        update["$set"]["password"] = hasher(password)
                        update["$set"]["security_check"] = datetime.now()

                    database.mongodb.suivicampagne.utilisateurs.update_one(filter, update)

                    response = HttpResponseRedirect(reverse("user-detail", kwargs = {"identifier" : identifier}))
                    # Si les informations de l'utilisateur actif sont modifiées, MAJ des cookies
                    if identifier == context["iduser"] :
                        response.set_cookie("isadmin", admin)
                        response.set_cookie("nom", name)
                        response.set_cookie("prenom", firstname)
                        response.set_cookie("email", email)
                else:
                    msg.add_message(request, msg.ERROR, form.errors)
                    response = HttpResponseRedirect(reverse("user-detail", kwargs = {"identifier" : identifier}))
            else:
                # Valeur de retour
                response = HttpResponseRedirect(reverse("user-detail", kwargs = {"identifier" : identifier}))
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

def delete_user(request, identifier) :
    if database.mongodb.isAlive() :
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "" :
            database.mongodb.suivicampagne.utilisateurs.delete_one({"_id" : ObjectId(identifier)})
            response = HttpResponseRedirect(reverse("list-user"))
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else :
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)
    return response
