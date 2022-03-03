import csv
from utils.database import mongodb
from datetime import datetime
from bson import ObjectId


def read_tsv():
    file = open("scripts/data/partenaires.tsv")
    csvreader = csv.reader(file, delimiter="\t")
    header = next(csvreader)
    if mongodb.isAlive():
        for row in csvreader:
            array_bases = []
            array_cat = []
            partner_name = row[0]
            contact_lastname = row[1]
            contact_firstname = row[2]
            contact_function = row[3]
            contact_email = row[4]
            contact_tel = row[5]
            contact_skype = row[6]
            comments = row[7]
            bases = row[9]
            if "INTERNE" in bases:
                array_bases.append("interne")
            elif "EXTERNE" in bases:
                array_bases.append("externe")

            if "T" in row[8]:
                co_reg = mongodb.suivicampagne.categories.find_one({"libelle": header[8]})
                array_cat.append(ObjectId(co_reg["_id"]))
            if "T" in row[10]:
                caritatives = mongodb.suivicampagne.categories.find_one({"libelle": header[10]})
                array_cat.append(ObjectId(caritatives["_id"]))
            if "T" in row[11]:
                e_commerce = mongodb.suivicampagne.categories.find_one({"libelle": header[11]})
                array_cat.append(ObjectId(e_commerce["_id"]))
            if "T" in row[12]:
                formation = mongodb.suivicampagne.categories.find_one({"libelle": header[12]})
                array_cat.append(ObjectId(formation["_id"]))
            if "T" in row[13]:
                minceur = mongodb.suivicampagne.categories.find_one({"libelle": header[13]})
                array_cat.append(ObjectId(minceur["_id"]))
            if "T" in row[14]:
                sondage = mongodb.suivicampagne.categories.find_one({"libelle": header[14]})
                array_cat.append(ObjectId(sondage["_id"]))
            if "T" in row[15]:
                defisc = mongodb.suivicampagne.categories.find_one({"libelle": header[15]})
                array_cat.append(ObjectId(defisc["_id"]))
            if "T" in row[16]:
                beaute = mongodb.suivicampagne.categories.find_one({"libelle": header[16]})
                array_cat.append(ObjectId(beaute["_id"]))
            if "T" in row[17]:
                voyage = mongodb.suivicampagne.categories.find_one({"libelle": header[17]})
                array_cat.append(ObjectId(voyage["_id"]))

            mongodb.suivicampagne.partenaires.insert_one({
                "siret": "",
                "nom_partenaire": partner_name,
                "nom_contact": contact_lastname,
                "prenom": contact_firstname,
                "fonction": contact_function,
                "email": contact_email,
                "telephone": contact_tel,
                "skype": contact_skype,
                "commentaire": comments,
                "bases": array_bases,
                "categories": array_cat,
                "datecreation": datetime.now(),
                "datemodification": datetime.now()
            })
    else:
        print("error")



if __name__ == "__main__":
    mongodb.openConnection()
    read_tsv()