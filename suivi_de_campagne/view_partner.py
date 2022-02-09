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


def list_partner(request):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            match = {"$match": {}}
            project = {"$project": {"nom_partenaire": 1, "nom_contact": 1, "prenom": 1, "fonction": 1, "email": 1,
                                    "telephone": 1, "skype": 1, "categories": 1, "siret": 1, "datecreation": 1,
                                    "datemodification": 1}}
            sort = {"$sort": {"nom_partenaire": 1}}
            partners_mongo = database.mongodb.suivicampagne.partenaires.aggregate([match, project, sort])
            partners = []
            for partenaire in partners_mongo:
                partenaire["id"] = partenaire["_id"]
                partners.append(partenaire)

            context["partenaires"] = partners
            response = render(request, "partner_list.html", context)
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        # Retour sur la mire de connexion
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)
    return response


def partner_detail(request, identifier=None):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            context["identifier"] = identifier

            # Partenaire existant
            if identifier:
                partner = database.mongodb.suivicampagne.partenaires.find_one({"_id": ObjectId(identifier)})
                if partner:
                    # Affichage de la page détails partenaire
                    values = {}
                    for key, value in partner.items():
                        values[key] = value
                    form = forms.PartnerForm(initial=values)
                    context["form"] = form
                    response = render(request, "partner_detail.html", context)
                else:
                    form = forms.PartnerForm()
                    context["erreur"] = messages.not_found
                    context["form"] = form
                    response = render(request, "partner_detail.html", context)
            else:
                form = forms.PartnerForm()
                context["form"] = form
                response = render(request, "partner_detail.html", context)
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


def create_partner(request):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            if request.method == "POST":
                # Validation du formulaire
                form = forms.PartnerForm(request.POST)
                if form.is_valid():
                    # Récupération des données
                    bases = form.cleaned_data["bases"]
                    contact_name = form.cleaned_data["nom_contact"]
                    firstname = form.cleaned_data["prenom"]
                    function = form.cleaned_data["fonction"]
                    email = form.cleaned_data["email"]
                    mobile = form.cleaned_data["telephone"]
                    skype = form.cleaned_data["skype"]
                    categories = form.cleaned_data["categories"]
                    siret = form.cleaned_data["siret"]
                    partner_name = form.cleaned_data["nom_partenaire"]

                    record = {
                        "bases": bases,
                        "nom_contact": contact_name,
                        "prenom": firstname,
                        "fonction": function,
                        "email": email,
                        "telephone": mobile,
                        "skype": skype,
                        "categories": categories,
                        "siret": siret,
                        "nom_partenaire": partner_name,
                        "datecreation": datetime.now(),
                        "datemodification": datetime.now()
                    }
                    identifier = database.mongodb.suivicampagne.partenaires.insert_one(
                        record).inserted_id
                    identifier = str(identifier)

                    # Valeur de retour
                    response = HttpResponseRedirect(reverse("partner-detail", kwargs={"identifier": identifier}))
                else:
                    msg.add_message(request, msg.ERROR, form.errors)
                    response = HttpResponseRedirect(reverse("partner-detail"))
            else:
                # Valeur de retour
                response = HttpResponseRedirect(reverse("partner-detail"))
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        # Retour sur la mire de connexion
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)

    return response


def edit_partner(request, identifier):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            if request.method == "POST":
                # Validation du formulaire
                form = forms.PartnerForm(request.POST)
                if form.is_valid():
                    # Récupération des données
                    bases = form.cleaned_data["bases"]
                    contact_name = form.cleaned_data["nom_contact"]
                    firstname = form.cleaned_data["prenom"]
                    function = form.cleaned_data["fonction"]
                    email = form.cleaned_data["email"]
                    mobile = form.cleaned_data["telephone"]
                    skype = form.cleaned_data["skype"]
                    categories = form.cleaned_data["categories"]
                    siret = form.cleaned_data["siret"]
                    partner_name = form.cleaned_data["nom_partenaire"]

                    filter = { "_id" : ObjectId(identifier) }
                    update = { 
                        "$set" : {
                            "bases": bases,
                            "nom_contact": contact_name,
                            "prenom": firstname,
                            "fonction": function,
                            "email": email,
                            "telephone": mobile,
                            "skype": skype,
                            "categories": categories,
                            "siret": siret,
                            "nom_partenaire": partner_name,
                            "datemodification": datetime.now()
                        }
                    }
                    database.mongodb.suivicampagne.partenaires.update_one(filter, update)

                    response = HttpResponseRedirect(reverse("partner-detail", kwargs={"identifier": identifier}))
                else:
                    msg.add_message(request, msg.ERROR, form.errors)
                    response = HttpResponseRedirect(reverse("partner-detail", kwargs={"identifier": identifier}))
            else:
                # Valeur de retour
                response = HttpResponseRedirect(reverse("partner-detail", kwargs={"identifier": identifier}))
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


def delete_partner(request, identifier):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            database.mongodb.suivicampagne.partenaires.delete_one({"_id": ObjectId(identifier)})
            response = HttpResponseRedirect(reverse("list-partner"))
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)
    return response
