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


def list_customer(request):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            match = {"$match": {}}
            project = {"$project": {"nom_entreprise": 1, "siret": 1, "datecreation": 1, "datemodification": 1}}
            sort = {"$sort": {"nom_partenaire": 1}}
            customers_mongo = database.mongodb.suivicampagne.clients.aggregate([match, project, sort])
            customers = []
            for customer in customers_mongo:
                customer["id"] = customer["_id"]
                customers.append(customer)

            context["clients"] = customers
            response = render(request, "customer_list.html", context)
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        # Retour sur la mire de connexion
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)
    return response


def customer_detail(request, identifier=None):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            context["identifier"] = identifier
            # Client existant
            if identifier:
                customer = database.mongodb.suivicampagne.clients.find_one({"_id": ObjectId(identifier)})
                if customer:
                    # Affichage de la page détails client
                    values = {}
                    for key, value in customer.items():
                        values[key] = value
                    form = forms.CustomerForm(initial=values)
                    context["form"] = form
                    response = render(request, "customer_detail.html", context)
                else:
                    form = forms.CustomerForm()
                    context["form"] = form
                    context = {"erreur": messages.not_found}
                    response = render(request, "customer_detail.html", context)
            else:
                form = forms.CustomerForm()
                context["form"] = form
                response = render(request, "customer_detail.html", context)
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


def create_customer(request):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            if request.method == "POST":
                # Validation du formulaire
                form = forms.CustomerForm(request.POST)
                if form.is_valid():
                    # Récupération des données
                    bases = form.cleaned_data["bases"]
                    contact_name = form.cleaned_data["nom"]
                    firstname = form.cleaned_data["prenom"]
                    function = form.cleaned_data["fonction"]
                    email = form.cleaned_data["email"]
                    mobile = form.cleaned_data["telephone_mobile"]
                    phone = form.cleaned_data["telephone_fixe"]
                    levers = form.cleaned_data["leviers"]
                    themes = form.cleaned_data["thematiques"]
                    themes_blacklist = form.cleaned_data["thematiques_blacklist"]
                    siret = form.cleaned_data["siret"]
                    customer_name = form.cleaned_data["nom_entreprise"]
                    comments = form.cleaned_data["commentaire"]
                    postal_code = form.cleaned_data["code_postal"]
                    record = {
                        "siret": siret,
                        "nom_entreprise": customer_name,
                        "bases": bases,
                        "nom": contact_name,
                        "prenom": firstname,
                        "fonction": function,
                        "email": email,
                        "telephone_mobile": mobile,
                        "telephone_fixe": phone,
                        "leviers": levers,
                        "thematiques": themes,
                        "thematiques_blacklist": themes_blacklist,
                        "code_postal": postal_code,
                        "commentaires": comments,
                        "datecreation": datetime.now(),
                        "datemodification": datetime.now()
                    }
                    identifier = database.mongodb.suivicampagne.clients.insert_one(
                        record).inserted_id
                    identifier = str(identifier)

                    # Valeur de retour
                    response = HttpResponseRedirect(reverse("customer-detail", kwargs={"identifier": identifier}))
                else:
                    msg.add_message(request, msg.ERROR, form.errors)
                    response = HttpResponseRedirect(reverse("customer-detail"))
            else:
                # Valeur de retour
                response = HttpResponseRedirect(reverse("customer-detail"))
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        # Retour sur la mire de connexion
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)
    return response


def edit_customer(request, identifier):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            if request.method == "POST":
                # Validation du formulaire
                form = forms.CustomerForm(request.POST)
                if form.is_valid():
                    # Récupération des données
                    bases = form.cleaned_data["bases"]
                    contact_name = form.cleaned_data["nom"]
                    firstname = form.cleaned_data["prenom"]
                    function = form.cleaned_data["fonction"]
                    email = form.cleaned_data["email"]
                    mobile = form.cleaned_data["telephone_mobile"]
                    phone = form.cleaned_data["telephone_fixe"]
                    levers = form.cleaned_data["leviers"]
                    themes = form.cleaned_data["thematiques"]
                    themes_blacklist = form.cleaned_data["thematiques_blacklist"]
                    siret = form.cleaned_data["siret"]
                    customer_name = form.cleaned_data["nom_entreprise"]
                    comments = form.cleaned_data["commentaire"]
                    postal_code = form.cleaned_data["code_postal"]

                    filter = {"_id": ObjectId(identifier)}
                    update = {
                        "$set": {
                            "siret": siret,
                            "nom_entreprise": customer_name,
                            "bases": bases,
                            "nom": contact_name,
                            "prenom": firstname,
                            "fonction": function,
                            "email": email,
                            "telephone_mobile": mobile,
                            "telephone_fixe": phone,
                            "leviers": levers,
                            "thematiques": themes,
                            "thematiques_blacklist": themes_blacklist,
                            "code_postal": postal_code,
                            "commentaires": comments,
                            "datemodification": datetime.now()
                        }
                    }
                    database.mongodb.suivicampagne.clients.update_one(filter, update)

                    response = HttpResponseRedirect(reverse("customer-detail", kwargs={"identifier": identifier}))
                else:
                    msg.add_message(request, msg.ERROR, form.errors)
                    response = HttpResponseRedirect(reverse("customer-detail", kwargs={"identifier": identifier}))
            else:
                # Valeur de retour
                response = HttpResponseRedirect(reverse("customer-detail", kwargs={"identifier": identifier}))
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


def delete_customer(request, identifier):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            database.mongodb.suivicampagne.clients.delete_one({"_id": ObjectId(identifier)})
            response = HttpResponseRedirect(reverse("list-customer"))
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)
    return response
