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
        context = {"erreur" : messages.error_database}
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
                response = redirect("partner-detail")
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


def partner_list(request):
    return ""


def partner_detail(request):
    return render(request, "partner-detail.html", {})
