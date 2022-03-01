from django.contrib import messages as msg
from django.shortcuts import render

from suivi_de_campagne import view_signin_signup_reset
from utils import database
from . import messages
from . import views


def home(request):
    if database.mongodb.isAlive():
        # Contexte générique
        context = views.context_processor(request)
        # Si utilisateur connecté
        if context["iduser"] != "":
            # match avec campagnes du mois en cours
            match = {"$match": {"statut": "LIVE"}}
            project = {"$project": {"libelle": 1, "statut": 1, "traffic_manager": 1, "client": 1, "datecreation": 1,
                                    "datemodification": 1, "objectif_mensuel": 1, "ca_realise": 1, "trend": 1,
                                    "trend_fin_mois": 1}}
            sort = {"$sort": {"libelle": 1}}
            lookup_uti = {"$lookup": {"from": "utilisateurs", "localField": "traffic_manager",
                                      "foreignField": "_id", "as": "traffic_manager"}}
            unwind_uti = {"$unwind": {"path": "$traffic_manager",
                                      "preserveNullAndEmptyArrays": True}}
            lookup_client = {"$lookup": {
                "from": "clients", "localField": "client", "foreignField": "_id", "as": "client"}}
            unwind_client = {"$unwind": {"path": "$client",
                                         "preserveNullAndEmptyArrays": True}}
            campaigns_mongo = database.mongodb.suivicampagne.campagnes.aggregate(
                [match, project, lookup_uti, lookup_client, unwind_uti, unwind_client, sort])
            campaigns = []
            for campaign in campaigns_mongo:
                campaign["id"] = campaign["_id"]
                if campaign["objectif_mensuel"] != None and campaign["objectif_mensuel"] != 0:
                    campaign["pourcentage_atteinte"] = round(
                        campaign["trend_fin_mois"] / campaign["objectif_mensuel"], 2)
                campaigns.append(campaign)
            context["campagnes"] = campaigns
            response = render(request, "home.html", context)
        else:
            # Retour sur la mire de connexion
            msg.add_message(request, msg.ERROR, messages.error_connect)
            response = view_signin_signup_reset.login_view(request, context)
    else:
        # Retour sur la mire de connexion
        msg.add_message(request, msg.ERROR, messages.error_database)
        response = view_signin_signup_reset.login_view(request)
    return response
