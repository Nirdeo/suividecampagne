from datetime import datetime

from bson import ObjectId
from django.contrib import messages as msg
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from suivi_de_campagne import view_signin_signup_reset
from utils import database, functions
from . import forms
from . import messages
from . import views
import pymongo


def list_campaign(request, archived = 0):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            context["archived"] = 0
            if archived == 1 :
                match = {"$match": {"statut" : "STOP"}}
                context["archived"] = 1
            else :
                match = {"$match": {"statut" : {"$ne" : "STOP"}}}
            project = {"$project": {"libelle": 1, "statut": 1, "traffic_manager" : 1, "client" : 1, "datecreation": 1, "datemodification": 1}}
            sort = {"$sort": {"libelle": 1}}
            lookup_uti = {"$lookup" : {"from" : "utilisateurs", "localField" : "traffic_manager", "foreignField" : "_id", "as" : "traffic_manager"}}
            unwind_uti = {"$unwind" : {"path" : "$traffic_manager", "preserveNullAndEmptyArrays": True}}
            lookup_client = {"$lookup" : {"from" : "clients", "localField" : "client", "foreignField" : "_id", "as" : "client"}}
            unwind_client = {"$unwind" : {"path" : "$client", "preserveNullAndEmptyArrays": True}}
            campaigns_mongo = database.mongodb.suivicampagne.campagnes.aggregate([match, project, lookup_uti, lookup_client, unwind_uti, unwind_client, sort])
            campaigns = []
            for campaign in campaigns_mongo:
                campaign["id"] = campaign["_id"]
                campaigns.append(campaign)

            context["campagnes"] = campaigns
            response = render(request, "campaign_list.html", context)
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        # Retour sur la mire de connexion
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)
    return response


def campaign_detail(request, identifier=None):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            context["identifier"] = identifier
            # Récupération des listes
            context["clients"] = list(database.mongodb.suivicampagne.clients.find({}, {"id" : "$_id", "nom_entreprise" : 1}).sort("nom_entreprise"))
            context["partenaires"] = list(database.mongodb.suivicampagne.partenaires.find({}, {"id" : "$_id", "nom_partenaire" : 1}).sort("nom_partenaire"))
            context["utilisateurs"] = list(database.mongodb.suivicampagne.utilisateurs.find({}, {"id" : "$_id", "nom" : 1, "prenom" : 1}).sort([("nom", pymongo.ASCENDING), ("prenom", pymongo.ASCENDING)]))
            context["leviers"] = list(database.mongodb.suivicampagne.leviers.find({}, {"id" : "$_id", "libelle" : 1}).sort("libelle"))
            context["modeles_eco"] = list(database.mongodb.suivicampagne.modeles_economiques.find({}, {"id" : "$_id", "libelle" : 1}).sort("libelle"))
            context["statuts"] = ["SETUP", "LIVE", "STOP"]
            context["jours_semaine"] = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

            # Campagne existante
            if identifier:
                campaign = database.mongodb.suivicampagne.campagnes.find_one({"_id": ObjectId(identifier)})
                if campaign:
                    # Affichage de la page détails campagne
                    values = {}
                    for key, value in campaign.items():
                        values[key] = value
                    form = forms.CampaignForm(initial=values)
                    context["form"] = form

                    # Informations et calculs
                    context["datemodification"] = campaign["datemodification"]
                    context["nb_jours"] = functions.calculs_campagne("nb_jours", campaign)
                    context["ca_campagne"] = functions.calculs_campagne("ca_campagne", campaign)
                    context["achat_realise"] = functions.calculs_campagne("achat_realise", campaign)
                    context["pourcentage_atteinte"] = functions.calculs_campagne("pourcentage_atteinte", campaign)
                    context["marge"] = functions.calculs_campagne("marge", campaign)
                    response = render(request, "campaign_detail.html", context)
                else:
                    form = forms.CampaignForm()
                    context["form"] = form
                    context = {"erreur": messages.not_found}
                    response = render(request, "campaign_detail.html", context)
            else:
                form = forms.CampaignForm()
                context["form"] = form
                response = render(request, "campaign_detail.html", context)
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


def create_campaign(request):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            if request.method == "POST":
                # Validation du formulaire
                form = forms.CampaignForm(request.POST)
                if form.is_valid():
                    # Récupération des données
                    name = form.cleaned_data["libelle"]
                    client = form.cleaned_data["client"]
                    partners = request.POST.getlist("partenaires")
                    collections = []
                    for partner in partners :
                        if partner != "" :
                            collections.append(ObjectId(partner))
                    traffic_manager = form.cleaned_data["traffic_manager"]
                    reporter = form.cleaned_data["reporter"]
                    commercial = form.cleaned_data["commercial"]
                    status = form.cleaned_data["statut"]
                    date_begin = form.cleaned_data["date_debut"]
                    date_end = form.cleaned_data["date_fin"]
                    # MAJ format dates pour mongo
                    date_begin = datetime.strptime(date_begin, "%d/%m/%Y")
                    date_end = datetime.strptime(date_end,"%d/%m/%Y")

                    lever = form.cleaned_data["levier"]
                    if lever != "" :
                        lever = ObjectId(lever)
                    modele_eco = form.cleaned_data["modele_eco"]
                    rate = form.cleaned_data["tarif"]
                    price_selling = form.cleaned_data["prix_vendu"]
                    price_set = form.cleaned_data["prix_defini"]
                    price_buying = form.cleaned_data["prix_achat"]
                    goal_monthly = form.cleaned_data["objectif_mensuel"]
                    goal_ca_month = form.cleaned_data["objectif_ca_mois"]
                    trend = form.cleaned_data["trend"]
                    trend_end_month = form.cleaned_data["trend_fin_mois"]
                    reporting_day = form.cleaned_data["jour_reporting"]
                    ca_achieved = form.cleaned_data["ca_realise"]
                    buying_achieved = form.cleaned_data["achat_realise"]
                    margin_achieved = form.cleaned_data["marge_realise"]
                    record = {
                        "libelle" : name,
                        "client" : ObjectId(client),
                        "partenaires" : collections,
                        "traffic_manager": ObjectId(traffic_manager),
                        "reporter": ObjectId(reporter),
                        "commercial": ObjectId(commercial),
                        "statut": status,
                        "date_debut": date_begin,
                        "date_fin": date_end,
                        "levier": lever,
                        "modele_eco": ObjectId(modele_eco),
                        "tarif": rate,
                        "prix_defini": price_set,
                        "prix_vendu" : price_selling,
                        "prix_achat" : price_buying,
                        "objectif_mensuel": goal_monthly,
                        "objectif_ca_mois": goal_ca_month,
                        "trend": trend,
                        "trend_fin_mois" : trend_end_month,
                        "jour_reporting": reporting_day,
                        "ca_realise" : ca_achieved,
                        "achat_realise" : buying_achieved,
                        "marge_realise" : margin_achieved,
                        "datecreation": datetime.now(),
                        "datemodification": datetime.now()
                    }
                    identifier = database.mongodb.suivicampagne.campagnes.insert_one(
                        record).inserted_id
                    identifier = str(identifier)

                    # Valeur de retour
                    response = HttpResponseRedirect(reverse("campaign-detail", kwargs={"identifier": identifier}))
                else:
                    msg.add_message(request, msg.ERROR, form.errors)
                    response = HttpResponseRedirect(reverse("campaign-detail"))
            else:
                # Valeur de retour
                response = HttpResponseRedirect(reverse("campaign-detail"))
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        # Retour sur la mire de connexion
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)
    return response


def edit_campaign(request, identifier):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            if request.method == "POST":
                # Validation du formulaire
                form = forms.CampaignForm(request.POST)
                if form.is_valid():
                    # Récupération des données
                    name = form.cleaned_data["libelle"]
                    client = form.cleaned_data["client"]
                    partners = request.POST.getlist("partenaires")
                    collections = []
                    for partner in partners :
                        if partner != "" :
                            collections.append(ObjectId(partner))
                    traffic_manager = form.cleaned_data["traffic_manager"]
                    reporter = form.cleaned_data["reporter"]
                    commercial = form.cleaned_data["commercial"]
                    status = form.cleaned_data["statut"]
                    date_begin = form.cleaned_data["date_debut"]
                    date_end = form.cleaned_data["date_fin"]
                    # MAJ format dates pour mongo
                    date_begin = datetime.strptime(date_begin, "%d/%m/%Y")
                    date_end = datetime.strptime(date_end,"%d/%m/%Y")

                    lever = form.cleaned_data["levier"]
                    if lever != "" :
                        lever = ObjectId(lever)
                    modele_eco = form.cleaned_data["modele_eco"]
                    rate = form.cleaned_data["tarif"]
                    price_selling = form.cleaned_data["prix_vendu"]
                    price_set = form.cleaned_data["prix_defini"]
                    price_buying = form.cleaned_data["prix_achat"]
                    goal_monthly = form.cleaned_data["objectif_mensuel"]
                    goal_ca_month = form.cleaned_data["objectif_ca_mois"]
                    trend = form.cleaned_data["trend"]
                    trend_end_month = form.cleaned_data["trend_fin_mois"]
                    reporting_day = form.cleaned_data["jour_reporting"]
                    ca_achieved = form.cleaned_data["ca_realise"]
                    buying_achieved = form.cleaned_data["achat_realise"]
                    margin_achieved = form.cleaned_data["marge_realise"]

                    filter = {"_id": ObjectId(identifier)}
                    update = {
                        "$set": {
                            "libelle" : name,
                            "client" : ObjectId(client),
                            "partenaires" : collections,
                            "traffic_manager": ObjectId(traffic_manager),
                            "reporter": ObjectId(reporter),
                            "commercial": ObjectId(commercial),
                            "statut": status,
                            "date_debut": date_begin,
                            "date_fin": date_end,
                            "levier": lever,
                            "modele_eco": ObjectId(modele_eco),
                            "tarif": rate,
                            "prix_defini" : price_set,
                            "prix_vendu" : price_selling,
                            "prix_achat" : price_buying,
                            "objectif_mensuel": goal_monthly,
                            "objectif_ca_mois": goal_ca_month,
                            "trend": trend,
                            "trend_fin_mois" : trend_end_month,
                            "jour_reporting": reporting_day,
                            "ca_realise" : ca_achieved,
                            "achat_realise" : buying_achieved,
                            "marge_realise" : margin_achieved,
                            "datemodification": datetime.now()
                        }
                    }
                    database.mongodb.suivicampagne.campagnes.update_one(filter, update)

                    response = HttpResponseRedirect(reverse("campaign-detail", kwargs={"identifier": identifier}))
                else:
                    msg.add_message(request, msg.ERROR, form.errors)
                    response = HttpResponseRedirect(reverse("campaign-detail", kwargs={"identifier": identifier}))
            else:
                # Valeur de retour
                response = HttpResponseRedirect(reverse("campaign-detail", kwargs={"identifier": identifier}))
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

def campaign_restore(request, identifier):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            # Restauration de la campagne
            filter = {"_id": ObjectId(identifier)}
            update = {
                "$set": {
                    "statut" : "LIVE",
                    "datemodification": datetime.now()
                }
            }
            database.mongodb.suivicampagne.campagnes.update_one(filter, update)

            # Récupération de la liste des campagnes non archivées
            match = {"$match": {"statut" : {"$ne" : "STOP"}}}
            project = {"$project": {"libelle": 1, "statut": 1, "traffic_manager" : 1, "client" : 1, "datecreation": 1, "datemodification": 1}}
            sort = {"$sort": {"libelle": 1}}
            lookup_uti = {"$lookup" : {"from" : "utilisateurs", "localField" : "traffic_manager", "foreignField" : "_id", "as" : "traffic_manager"}}
            unwind_uti = {"$unwind" : {"path" : "$traffic_manager", "preserveNullAndEmptyArrays": True}}
            lookup_client = {"$lookup" : {"from" : "clients", "localField" : "client", "foreignField" : "_id", "as" : "client"}}
            unwind_client = {"$unwind" : {"path" : "$client", "preserveNullAndEmptyArrays": True}}
            campaigns_mongo = database.mongodb.suivicampagne.campagnes.aggregate([match, project, lookup_uti, lookup_client, unwind_uti, unwind_client, sort])
            campaigns = []
            for campaign in campaigns_mongo:
                campaign["id"] = campaign["_id"]
                campaigns.append(campaign)

            context["campagnes"] = campaigns
            response = render(request, "campaign_list.html", context)
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


def delete_campaign(request, identifier):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            database.mongodb.suivicampagne.campagnes.delete_one({"_id": ObjectId(identifier)})
            response = HttpResponseRedirect(reverse("list-campaign"))
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)
    return response
