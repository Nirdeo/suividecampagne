from utils.functions import import_configuration, mark, hasher, uid_super_user
from pymongo import MongoClient
import datetime

mark("Initialisation de la base de données")

server = MongoClient(import_configuration("mongodb", "url"))
database = server["suivicampagne"]

server.drop_database("suivicampagne")

mark("Création des utilisateurs")
users = database["utilisateurs"]
users.drop()

registration = {
    "civilite" : "Mr",
    "nom" : "Super administrateur",
    "prenom" : "",
    "description" : "",
    "avatar" : "",
    "email" : import_configuration("superutilisateur"),
    "password" : hasher("onnejouepasaveclasecurite"),
    "security_check" : datetime.datetime.now(),
    "datecreation" : datetime.datetime.now(),
    "datemodification" : datetime.datetime.now()
}
users.insert_one(registration)
registration = {
    "civilite" : "Mme",
    "nom" : "Flamant",
    "prenom" : "Morgane",
    "description" : "",
    "avatar" : "",
    "email" : "mflamant@neptunemedia.fr",
    "password" : hasher("onnejouepasaveclasecurite"),
    "security_check" : datetime.datetime.now(),
    "datecreation" : datetime.datetime.now(),
    "datemodification" : datetime.datetime.now()
}
users.insert_one(registration)
registration = {
    "civilite" : "Mr",
    "nom" : "De Domenico",
    "prenom" : "Victor",
    "description" : "",
    "avatar" : "",
    "email" : "vdomenico@neptunemedia.fr",
    "password" : hasher("onnejouepasaveclasecurite"),
    "security_check" : datetime.datetime.now(),
    "datecreation" : datetime.datetime.now(),
    "datemodification" : datetime.datetime.now()
}
users.insert_one(registration)

mark("Création du tracking")
tracking = database["tracking"]
tracking.drop()
enregistrement = {
    "libelle" : "Initialisation de l'application",
    "utilisateur" : uid_super_user(),
    "timestamp" : datetime.datetime.now(),
}
tracking.insert_one(enregistrement)