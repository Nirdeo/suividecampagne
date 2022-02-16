"""
    Bibliothèque de fonctions génériques pour le projet suivi de campagnes
    Dernière modification : 2022-01-24 (MF)
"""
import json
import hashlib
import string
import random
import smtplib
from datetime import datetime
from os import chmod
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
        absolute_path = directory + "suividecampagne." + datetime.now().strftime("%Y%m%d") + ".log"
        print(message)
        with open(absolute_path, "a", encoding="utf8") as log:
            log.write(datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ") + message + "\n")
        chmod(absolute_path, 0o777)
        return_value = True
    except Exception as error:
        print(" ! Une erreur s'est produite durant 'mark' : {} {}".format(error, type(error)))
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
            print(" ! Une erreur s'est produite durant 'envoyer_email' : {} {}".format(error, type(error)))
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
        data = collection.find_one({"email": import_configuration("superutilisateur")})
        return_value = data["_id"]
    except Exception as error:
        print("Une erreur s'est produite durant 'uid_super_utilisateur' : {} {}".format(error, type(error)))
        return_value = ""
    return return_value

def calculs_campagne(key, campaign) :
    # TODO : récupérer résultats tradedoubler
    count_leads = 100
    count_clicks = 236
    count_affiliates = 34

    model_eco = database.mongodb.suivicampagne.modeles_economiques.find_one({"_id": campaign["modele_eco"]})
    # Calculs
    if campaign["prix_vendu"] != None and campaign["prix_defini"] != None :
        if model_eco["libelle"] == "CTL" :
            ca = count_leads * campaign["prix_vendu"]
            marge = count_leads * campaign["prix_defini"]
        elif model_eco["libelle"] == "CPL" :
            ca = count_leads * campaign["prix_vendu"]
            marge = count_leads * campaign["prix_defini"]
        elif model_eco["libelle"] == "CPC" :
            ca = count_clicks * campaign["prix_vendu"]
            marge = count_clicks * campaign["prix_defini"]
        elif model_eco["libelle"] == "CPA" :
            ca = count_affiliates * campaign["prix_vendu"]
            marge = count_affiliates * campaign["prix_defini"]
    else :
        ca = 0
        marge = 0

    if key == "nb_jours" :
        nb_jours = campaign["date_fin"] - campaign["date_debut"]
        nb_jours_str = str(nb_jours.days) + " jours"
        return nb_jours_str
    elif key == "pourcentage_atteinte" :
        if campaign["objectif_mensuel"] != None and campaign["objectif_mensuel"] != 0 :
            return round(campaign["trend_fin_mois"] / campaign["objectif_mensuel"], 2)
        else :
            return 0

    elif key == "ca_campagne" :
        return ca

    elif key == "achat_realise" :
        return marge

    elif key == "marge" and campaign["prix_achat"] is not None:
        return ca - campaign["prix_achat"]
    else :
        return "clef non trouvée"
