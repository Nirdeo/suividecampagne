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
    "civilite": "Mr",
    "nom": "Super administrateur",
    "prenom": "",
    "description": "",
    "avatar": "",
    "email": import_configuration("superutilisateur"),
    "password": hasher("onnejouepasaveclasecurite"),
    "security_check": datetime.datetime.now(),
    "datecreation": datetime.datetime.now(),
    "datemodification": datetime.datetime.now()
}
uid_superuser = users.insert_one(registration).inserted_id
registration = {
    "civilite": "Mme",
    "nom": "Flamant",
    "prenom": "Morgane",
    "description": "",
    "avatar": "",
    "email": "mflamant@neptunemedia.fr",
    "password": hasher("onnejouepasaveclasecurite"),
    "security_check": datetime.datetime.now(),
    "datecreation": datetime.datetime.now(),
    "datemodification": datetime.datetime.now()
}
users.insert_one(registration)
registration = {
    "civilite": "Mr",
    "nom": "De Domenico",
    "prenom": "Victor",
    "description": "",
    "avatar": "",
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
themes_blacklist = database.create_collection("themes_blacklist")

mark("Création des leviers")
leviers = database.create_collection("leviers")

mark("Création des partenaires")
partenaires = database.create_collection("partenaires")

mark("Création des clients")
clients = database.create_collection("clients")

