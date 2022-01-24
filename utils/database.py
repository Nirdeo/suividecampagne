from pymongo import MongoClient

from utils.functions import import_configuration


class mongodb(object):

    def openConnection(self=None):
        try:
            uri = import_configuration("mongodb", "url")
            mongodb.client = MongoClient(uri)
            mongodb.suivicampagne = mongodb.client.suivicampagne
        except Exception as error:
            # print("[ ! ] Exception database.mongodb.openConnection() : {0} {1}".format(error, type(error)))
            mongodb.client = None
            mongodb.suivicampagne = None

    def closeConnection(self=None):
        try:
            mongodb.client.close()
            mongodb.suivicampagne = None
        except Exception as error:
            # print("[ ! ] Exception database.mongodb.closeConnection() : {0} {1}".format(error, type(error)))
            mongodb.client = None
            mongodb.suivicampagne = None

    def isAlive(self=None):
        try:
            mongodb.client.server_info()
            return True
        except Exception as error:
            # print("[ ! ] Exception database.mongodb.isAlive() : {0} {1}".format(error, type(error)))
            return False
