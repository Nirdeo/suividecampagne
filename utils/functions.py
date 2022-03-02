"""
    Bibliothèque de fonctions génériques pour le projet suivi de campagnes
    Dernière modification : 2022-01-24 (MF)
"""
import hashlib
import json
import random
import smtplib
import string
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import chmod

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

from utils import database


def import_configuration(section, key=""):
    """
    Fonction qui renvoit un élément du fichier de configuration
    """
    try:
        with open(f"campagne.config.json", "r") as json_file:
            data = json.load(json_file)
        if key != "":
            return_value = data[section][key]
        else:
            return_value = data[section]
    except Exception as error:
        print(" ! Une erreur s'est produite durant 'import_configuration' : {} {}".format(
            error, type(error)))
        return_value = ""
    return return_value


def hasher(string, algorithm="SHA256"):
    """
    Fonction qui renvoit une chaîne encodée via l'algorithme SHA-256
    """
    try:
        encoded_string = str.encode(string)
        if algorithm == "MD5":
            MD5 = hashlib.md5()
            MD5.update(encoded_string)
            return_value = MD5.hexdigest()
        else:
            SHA256 = hashlib.sha256()
            SHA256.update(encoded_string)
            return_value = SHA256.hexdigest()
    except Exception as error:
        print(" ! Une erreur s'est produite durant 'hasher' : {} {}".format(
            error, type(error)))
        return_value = ""
    return return_value


def generate_password(size=12, chars=string.ascii_letters + string.digits):
    """
    Fonction qui génère un mot de passe aléatoire
    """
    return "".join(random.choice(chars) for _ in range(size))


def mark(message=""):
    """
    Procédure qui affiche dans la console, et écrit en même temps dans le fichier suividecampagne.log
    """
    try:
        directory = import_configuration("repertoire", "log")
        absolute_path = directory + "suividecampagne." + \
                        datetime.now().strftime("%Y%m%d") + ".log"
        print(message)
        with open(absolute_path, "a", encoding="UTF8") as log:
            log.write(datetime.now().strftime(
                "[%Y-%m-%d %H:%M:%S] ") + message + "\n")
        chmod(absolute_path, 0o777)
        return_value = True
    except Exception as error:
        print(" ! Une erreur s'est produite durant 'mark' : {} {}".format(
            error, type(error)))
        return_value = False
    return return_value


def send_email(destinataire, sujet, contenu):
    """
    Fonction qui envoie un e-mail
    """
    if import_configuration("email", "active") == True:
        server_address = import_configuration("smtp", "host")
        server_port = import_configuration("smtp", "port")
        server_login = import_configuration("smtp", "username")
        server_password = import_configuration("smtp", "password")
        sender = import_configuration("smtp", "sender")

        message = MIMEMultipart("alternative")
        message["From"] = sender
        message["Subject"] = sujet
        html = contenu
        part = MIMEText(html, "html")
        message.attach(part)
        try:
            server = smtplib.SMTP(server_address, server_port, server_address)
            server.starttls()
            server.ehlo()
            server.login(server_login, server_password)
            server.sendmail(message["From"], destinataire, message.as_string())
            server.quit()
            return_value = True
        except Exception as error:
            print(" ! Une erreur s'est produite durant 'envoyer_email' : {} {}".format(
                error, type(error)))
            return_value = False
    else:
        print(" ! Envoi d'email désactivé")
        return_value = False
    return return_value


def tracking(label, user=None):
    """
    Fonction qui créé un élément de tracking
    """
    registration = {
        "libelle": label,
        "utilisateur": user,
        "timestamp": datetime.now(),
    }
    server = MongoClient(import_configuration("mongodb", "url"))
    database = server["suivicampagne"]
    database["tracking"].insert_one(registration)


def uid_super_user():
    """
    Fonction qui va chercher l'uid du superutilisateur
    """
    try:
        server = MongoClient(import_configuration("mongodb", "url"))
        database = server["suivicampagne"]
        collection = database["utilisateurs"]
        data = collection.find_one(
            {"email": import_configuration("superutilisateur")})
        return_value = data["_id"]
    except Exception as error:
        print("Une erreur s'est produite durant 'uid_super_utilisateur' : {} {}".format(
            error, type(error)))
        return_value = ""
    return return_value


def get_value_tradedoubler(url) :
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    value = soup.find_all("td", class_="bS aR")
    value = int(value[-1].string.replace('\xa0', ''))
    return value

def get_all_values_tradedoubler(id_tradedoubler, date_debut, date_fin) :
    # Généralités
    url = import_configuration("tradedoubler", "url")
    values = {}
    parameters_campaign = ""
    parameters_campaign += "&startDate=" + date_debut.strftime("%d/%m/%y")
    parameters_campaign += "&endDate=" + date_fin.strftime("%d/%m/%y")
    parameters_campaign += "&programId=" + str(id_tradedoubler)
    parameters_campaign += "&metric1.lastOperator=/&interval=MONTHS&currencyId=EUR&run_as_organization_id=2294738&metric1.summaryType=NONE&latestDayToExecute=0&metric1.operator1=/&reportTitleTextKey=REPORT3_SERVICE_REPORTS_MMERCHANTOVERVIEWREPORT_TITLE&metric1.columnName1=siteId&setColumns=true&metric1.columnName2=siteId&decorator=popupDecorator&metric1.midOperator=/&viewType=1&tabMenuName=TABMENU_MERCHANT_PROGRAM_REPORTS_OVERVIEW&allPrograms=false&customKeyMetricCount=0&applyNamedDecorator=true&programIds=" + str(id_tradedoubler) + "&key=640aae6b412f2611bd555087c381c887&format=HTML"

    # nb clicks
    url_nbclicks = url + "&columns=clickNrOf" + parameters_campaign
    values["count_clicks_tradedoubler"] = get_value_tradedoubler(url_nbclicks)

    # nb clicks unique
    url_nbclicks_uniques = url + "&columns=uvNrOf" + parameters_campaign
    values["count_unique_clicks_tradedoubler"] = get_value_tradedoubler(url_nbclicks_uniques)

    # Leads
    url_leads = url + "&columns=leadNrOf" + parameters_campaign
    values["count_leads_tradedoubler"] = get_value_tradedoubler(url_leads)

    # Mille
    url_mille = url + "&columns=saleNrOf" + parameters_campaign
    values["count_mille_tradedoubler"] = get_value_tradedoubler(url_mille)

    return values

def calculs_campagne(campaign):
    campaign_calc = {}
    model_eco = database.mongodb.suivicampagne.modeles_economiques.find_one(
        {"_id": campaign["modele_eco"]})
    # Récupération des informations de tradedoubler si id tradedoubler
    values = {
        "count_clicks" : campaign["nb_cliques"],
        "count_unique_clicks" : campaign["nb_cliques_uniques"],
        "count_leads" : campaign["nb_leads"],
        "count_affiliates" : campaign["nb_affiliates"],
        "count_mille" : campaign["nb_ventes"]
    }
    if campaign["id_tradedoubler"] != None :
        tradedoubler_values = get_all_values_tradedoubler(campaign["id_tradedoubler"], campaign["date_debut"], campaign["date_fin"])
        values.update(tradedoubler_values)
        campaign_calc["tradedoubler_values"] = tradedoubler_values

    ca = 0
    achats = 0

    # Calculs CA / achats / marge
    if campaign["prix_vendu"] != None and campaign["prix_achat"] != None :
        if model_eco["libelle"] == "CTL":
            # Valeurs manuelles
            if "count_leads" in values and values["count_leads"] != None :
                ca = values["count_leads"] * campaign["prix_vendu"]
                achats = values["count_leads"] * campaign["prix_achat"]
            # Valeurs tradedoubler
            elif "count_leads_tradedoubler" in values and values["count_leads_tradedoubler"] != None :
                ca = values["count_leads_tradedoubler"] * campaign["prix_vendu"]
                achats = values["count_leads_tradedoubler"] * campaign["prix_achat"]
        elif model_eco["libelle"] == "CPL":
           # Valeurs manuelles
            if "count_leads" in values and values["count_leads"] != None :
                ca = values["count_leads"] * campaign["prix_vendu"]
                achats = values["count_leads"] * campaign["prix_achat"]
            # Valeurs tradedoubler
            elif "count_leads_tradedoubler" in values and values["count_leads_tradedoubler"] != None :
                ca = values["count_leads_tradedoubler"] * campaign["prix_vendu"]
                achats = values["count_leads_tradedoubler"] * campaign["prix_achat"]
        elif model_eco["libelle"] == "CPC":
            # Valeurs manuelles
            if "count_unique_clicks" in values and values["count_unique_clicks"] != None :
                ca = values["count_unique_clicks"] * campaign["prix_vendu"]
                achats = values["count_unique_clicks"] * campaign["prix_achat"]
            # Valeurs tradedoubler
            elif "count_unique_clicks_tradedoubler" in values and values["count_unique_clicks_tradedoubler"] != None  :
                ca = values["count_unique_clicks_tradedoubler"] * campaign["prix_vendu"]
                achats = values["count_unique_clicks_tradedoubler"] * campaign["prix_achat"]
        elif model_eco["libelle"] == "CPA":
            # Valeurs manuelles
            ca = values["count_affiliates"] * campaign["prix_vendu"]
            achats = values["count_affiliates"] * campaign["prix_achat"]
        elif model_eco["libelle"] == "CPM":
            # Valeurs manuelles
            if "count_mille" in values and values["count_mille"] != None :
                ca = values["count_mille"] * campaign["prix_vendu"]
                achats = values["count_mille"] * campaign["prix_achat"]
            # Valeurs tradedoubler
            elif "count_mille_tradedoubler" in values and values["count_mille_tradedoubler"] != None :
                ca = values["count_mille_tradedoubler"] * campaign["prix_vendu"]
                achats = values["count_mille_tradedoubler"] * campaign["prix_achat"]

    campaign_calc["ca_campagne"] = ca
    campaign_calc["achat_realise"] = achats
    campaign_calc["marge"] = ca - achats

    # nb jours
    nb_jours = campaign["date_fin"] - campaign["date_debut"]
    campaign_calc["nb_jours"] = str(nb_jours.days) + " jours"
    # poucentage d'atteinte
    if campaign["objectif_mensuel"] != None and campaign["objectif_mensuel"] != 0:
        campaign_calc["pourcentage_atteinte"] = round(campaign["trend_fin_mois"] / campaign["objectif_mensuel"], 2)
    else:
        campaign_calc["pourcentage_atteinte"] = 0

    return campaign_calc
