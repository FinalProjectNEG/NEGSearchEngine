from pymongo import MongoClient, errors
import re

def Get_Information(word):

    cluster = MongoClient("mongodb://localhost:27017")
    cluster.server_info()
    db = cluster["NEG"]
    if word in db.list_collection_names():

        print("helooooooooooooooooooooooooooo")
        col = db[word]
        x = col.find()
        #return object type 'cursor' and when we go through the parameter by loop (for) we get dictionary
        return x

    return None

def Get_Graph():

    cluster = MongoClient("mongodb://localhost:27017")
    db = cluster["Links"]
    collection = db["Graph"]
    k = collection.find()
    return k

def listDB(list_words):
    cluster = MongoClient("mongodb://localhost:27017")
    cluster.server_info()
    db = cluster["NEG"]
    list_final = []
    for word in list_words:
        r=re.compile(".*"+word+".*")
        new_list = list(filter(r.match,db.list_collection_names()))
        list_final.extend(new_list)

    return list_final


