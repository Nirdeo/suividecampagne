import datetime

from pymongo import MongoClient

from utils.functions import import_configuration, mark, hasher

mark("Initialisation de la base de données")

# Connexion au serveur MongoDB
server = MongoClient(import_configuration("mongodb", "url"))
database = server["suivicampagne"]

server.drop_database("suivicampagne")

mark("Création des utilisateurs")
users = database["utilisateurs"]
users.drop()

registration = {
    "admin" : True,
    "civilite": "Mr",
    "nom": "Super administrateur",
    "prenom": "",
    "description": "",
    "email": import_configuration("superutilisateur"),
    "password": hasher("onnejouepasaveclasecurite"),
    "security_check": datetime.datetime.now(),
    "datecreation": datetime.datetime.now(),
    "datemodification": datetime.datetime.now()
}
uid_superuser = users.insert_one(registration).inserted_id
registration = {
    "admin" : True,
    "civilite": "Mme",
    "nom": "Flamant",
    "prenom": "Morgane",
    "description": "",
    "email": "mflamant@neptunemedia.fr",
    "password": hasher("onnejouepasaveclasecurite"),
    "security_check": datetime.datetime.now(),
    "datecreation": datetime.datetime.now(),
    "datemodification": datetime.datetime.now()
}
users.insert_one(registration)
registration = {
    "admin" : True,
    "civilite": "Mr",
    "nom": "De Domenico",
    "prenom": "Victor",
    "description": "",
    "email": "vdomenico@neptunemedia.fr",
    "password": hasher("onnejouepasaveclasecurite"),
    "security_check": datetime.datetime.now(),
    "datecreation": datetime.datetime.now(),
    "datemodification": datetime.datetime.now()
}
users.insert_one(registration)

mark("Création du tracking")
tracking = database["tracking"]
tracking.drop()
record = {
    "libelle": "Initialisation de l'application",
    "utilisateur": uid_superuser,
    "timestamp": datetime.datetime.now(),
}
tracking.insert_one(record)
mark("Création des thèmes")
themes = database.create_collection("themes")

mark("Création de la liste noire des thèmes")
themes_blacklist = database.create_collection("themes_liste_noire")

mark("Création des leviers")
levers = database.create_collection("leviers")

mark("Création des partenaires")
partenaires = database.create_collection("partenaires")

mark("Création des clients")
customers = database["clients"]
# Jeu d'essai client
registration = {
    "siret": "47931411400022",
    "nom_entreprise": "Neptune Media",
    "bases": "interne",
    "nom": "DRIANCOURT",
    "prenom": "Nicolas",
    "fonction": "Responsable du service informatique",
    "email": "ndriancourt@neptunemedia.fr",
    "telephone_mobile": "",
    "telephone_fixe": "01 44 52 84 17",
    "skype" : "",
    "leviers": "",
    "thematiques": "",
    "thematiques_blacklist": "",
    "code_postal": "75010",
    "commentaires": "",
    "datecreation": datetime.datetime.now(),
    "datemodification": datetime.datetime.now()
}
client_jeu = customers.insert_one(registration).inserted_id

mark("Création des modèles économiques")
# Jeu d'essai modèles écos
economic_models = database["modeles_economiques"]
economic_models.drop()
registration = {
    "libelle" : "CPL",
    "datecreation" : datetime.datetime.now(),
}
modele_jeu = economic_models.insert_one(registration).inserted_id
registrations = [
    {
    "libelle" : "CPC",
    "datecreation" : datetime.datetime.now(),
    },
    {
    "libelle" : "CPA",
    "datecreation" : datetime.datetime.now(),
    },
    {
    "libelle" : "CPM",
    "datecreation" : datetime.datetime.now(),
    },
]
economic_models.insert_many(registrations)

mark("Création des campagnes")
campaigns = database["campagnes"]
campaigns.drop()

# Jeu d'essai campagne
registration = {
    "libelle" : "Campagne numéro 1",
    "id_tradedoubler" : 320282,
    "client" : client_jeu,
    "partenaires" : [],
    "traffic_manager": uid_superuser,
    "reporter": uid_superuser,
    "commercial": uid_superuser,
    "statut": "SETUP",
    "date_debut": datetime.datetime.now(),
    "date_fin": datetime.datetime.now(),
    "levier": "",
    "modele_eco": modele_jeu,
    "tarif": 1389,
    "prix_vendu" : 1388,
    "prix_achat" : 200,
    "objectif_mensuel": 1200,
    "objectif_ca_mois": 200,
    "nb_leads" : None,
    "nb_cliques" : None,
    "nb_cliques_uniques" : None,
    "nb_ventes" : None,
    "nb_affiliates" : None,
    "trend": 1000,
    "trend_fin_mois" : 0,
    "jour_reporting": "vendredi",
    "ca_realise" : False,
    "achat_realise" : False,
    "marge_realise" : False,
    "datecreation": datetime.datetime.now(),
    "datemodification": datetime.datetime.now()
}
campaigns.insert_one(registration)
