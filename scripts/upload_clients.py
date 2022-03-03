import csv
from utils.database import mongodb
from datetime import datetime


def read_tsv():
    file = open("scripts/data/clients.tsv")
    csvreader = csv.reader(file, delimiter="\t")
    next(csvreader)

    if mongodb.isAlive():
        for row in csvreader:
            denomination = row[0]
            mongodb.suivicampagne.clients.insert_one({
                "nom_entreprise": denomination,
                "datecreation": datetime.now(),
                "datemodification": datetime.now()
            })
    else:
        print("error")



if __name__ == "__main__":
    mongodb.openConnection()
    read_tsv()