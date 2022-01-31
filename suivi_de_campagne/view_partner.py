from datetime import datetime
from bson import ObjectId
from django.contrib import messages as msg
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from utils import database
from . import forms
from . import messages
from . import views


def view_partner(request):
    if database.mongodb.isAlive():
        # Affichage de la page partenaire
        form = forms.PartnerForm(request.POST)
        return render(request, "partner_create.html", {"form": form})
    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_database}
        return render(request, "login.html", context)


def create_partner(request):
    if database.mongodb.isAlive():
        if request.method == "POST":
            # Validation du formulaire
            form = forms.PartnerForm(request.POST)
            if form.is_valid():
                # Contexte générique
                context = views.context_processor(request)

                # Récupération des données
                base = form.cleaned_data["base"]
                nom_contact = form.cleaned_data["nom_contact"]
                prenom = form.cleaned_data["prenom"]
                fonction = form.cleaned_data["fonction"]
                email = form.cleaned_data["email"]
                telephone = form.cleaned_data["telephone"]
                skype = form.cleaned_data["skype"]
                categories = form.cleaned_data["categories"]
                siret = form.cleaned_data["siret"]
                nom_partenaire = form.cleaned_data["nom_partenaire"]

                identifiant = request.POST.get("identifiant")
                if identifiant != "":
                    enregistrement = {
                        "base": base,
                        "nom_contact": nom_contact,
                        "prenom": prenom,
                        "fonction": fonction,
                        "email": email,
                        "telephone": telephone,
                        "skype": skype,
                        "categories": categories,
                        "siret": siret,
                        "nom_partenaire": nom_partenaire,
                        "datecreation": datetime.now(),
                        "datemodification": datetime.now()
                    }
                    identifiant = database.mongodb.suivicampagne.partenaires.insert_one(
                        enregistrement).inserted_id
                    identifiant = str(identifiant)

                # Valeur de retour
                response = redirect("detail-partner")
            else:
                msg.add_message(request, msg.ERROR, form.errors)
                response = HttpResponseRedirect(reverse("create-partner"))
        else:
            # Valeur de retour
            response = HttpResponseRedirect(reverse("create-partner"))

    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_database}
        response = render(request, "login.html", context)

    # Fin de fonction
    return response


def detail_partner(request):
    return render(request, "partner_detail.html", {})


def list_partner(request):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        match = {"$match": {}}
        project = {"$project": {"nom_partenaire": 1, "nom_contact": 1, "prenom": 1, "fonction": 1, "email": 1,
                                "telephone": 1, "skype": 1, "categories": 1, "siret": 1, "datecreation": 1, "datemodification": 1}}
        sort = {"$sort": {"nom_partenaire": 1}}
        context["partenaires"] = database.mongodb.suivicampagne.partenaires.aggregate([match, project, sort])
        # Valeur de retour
        return render(request, "partner_list.html", context)
    else:
        # Retour sur la mire de connexion
        context = {"erreur": messages.error_database}
        return render(request, "login.html", context)
