import csv
from utils.database import mongodb
from datetime import datetime


def read_tsv():
    file = open("scripts/data/themes.tsv")
    csvreader = csv.reader(file, delimiter="\t")
    next(csvreader)

    if mongodb.isAlive():
        for row in csvreader:
            theme = row[0]
            mongodb.suivicampagne.themes.insert_one({
                "libelle": theme,
                "datecreation": datetime.now(),
                "datemodification": datetime.now()
            })
            mongodb.suivicampagne.categories.insert_one({
                "libelle": theme,
                "datecreation": datetime.now(),
                "datemodification": datetime.now()
            })
    else:
        print("error")



if __name__ == "__main__":
    mongodb.openConnection()
    read_tsv()