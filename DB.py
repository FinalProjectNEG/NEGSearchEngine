from pymongo import MongoClient


def Get_Information(word):

    cluster = MongoClient("mongodb+srv://neg:14563258@cluster0.dl8z8.mongodb.net/neg?retryWrites=true&w=majority")
    db = cluster["NEG"]
    if word in db.list_collection_names():
        col = db[word]
        x = col.find()
        #return object type 'cursor' and when we go through the parameter by loop (for) we get dictionary
        return x

def Get_Graph():

    cluster = MongoClient("mongodb+srv://neg:14563258@cluster0.dl8z8.mongodb.net/neg?retryWrites=true&w=majority")
    db = cluster["Links"]
    collection = db["Graph"]
    k = collection.find()
    return k



