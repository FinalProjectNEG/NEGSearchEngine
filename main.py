import nltk as nltk
from nltk.tokenize.regexp import WordPunctTokenizer
from DB import Get_Information, Get_Graph
from Url_Address import Url
from LSIModel import LSIModel
import math
from nltk.stem.porter import PorterStemmer


stopwords = nltk.corpus.stopwords.words('english')
# for tokenize the text from the page
tokenizer = WordPunctTokenizer()
stemmer = PorterStemmer()



def GruopWord(listtword, word, obj):
    # copy of list of words
    list_temp = listtword.copy()
    if word in listtword:
        list_temp.remove(word)

    for word1 in list_temp:
        if(word1 in obj.dictionary_word.keys()):
            return True

    return False


def SSearch(query):
    # do tokenize to the query, split_query is list
    tokens = tokenizer.tokenize(query)
    dictionary={}

    if len(tokens) > 1:
        # remove stopwords that not include DB
        clean = [token.lower() for token in tokens if token.lower() not in stopwords and len(token) > 2]
    else:
        clean = tokens.copy()
    final = [stemmer.stem(word) for word in clean]
    print("final: ",final)
    for word in final:
        cursor = Get_Information(word)
        if cursor == None:
            continue
        # Go through all the documents in the same word(collection)
        for diction in cursor:
            document = Url(diction.get('url'), diction.get('title'), diction.get('description'),
                           diction.get('appearance'), diction.get('word in page'))

            if document.url in dictionary.keys():
                if dictionary.get(document.url).title != None:
                    if word.lower() in dictionary.get(document.url).title.lower():
                        dictionary.get(document.url).appear_word_title.append(True)
                    else:
                        dictionary.get(document.url).appear_word_title.append(False)

                if dictionary.get(document.url).description != None:
                    if word.lower() in dictionary.get(document.url).description.lower():
                        dictionary.get(document.url).appear_word_description.append(True)
                    else:
                        dictionary.get(document.url).appear_word_description.append(False)
            else:
                if document.title != None:
                    print(document.title)
                    if word.lower() in document.title.lower():
                        document.appear_word_title.append(True)
                    else:
                        document.appear_word_title.append(False)
                if document.description != None:
                    if word.lower() in document.description.lower():
                        document.appear_word_description.append(True)
                    else:
                        document.appear_word_description.append(False)
                dictionary[document.url] = document

    for key in dictionary:
        if dictionary.get(key).title != None:
            temp_title = dictionary.get(key).appear_word_title
            true_title = temp_title.count(True)
            per_score_title = float(10 / len(temp_title))
            final_score_title = math.floor(true_title * per_score_title)
            dictionary.get(key).score += final_score_title


        if dictionary.get(key).description != None:
            temp_description = dictionary.get(key).appear_word_description
            true_description = temp_description.count(True)
            per_score_description = 7 / len(temp_description)
            final_score_description = math.floor(true_description * per_score_description)
            dictionary.get(key).score += final_score_description

    return dictionary





# function get our search query and we split it and search in the database, after that we look for the link with the heighest count of word that we lookin.
def Search_Query(query):

    #do tokenize to the query, split_query is list
    tokens = tokenizer.tokenize(query)

    if len(tokens)>1:
        #remove stopwords that not include DB
        clean = [token.lower() for token in tokens if token.lower() not in stopwords and len(token) > 2]
    else:
        clean = tokens.copy()

    dictionaryRel = {}
    dictionaryPartRel = {}
    print(clean)


    for word in clean:
        print(word)
        cursor = Get_Information(word)
        if cursor == None:
            print("can't find !")
            exit(-1)
        #Go through all the documents in the same word(collection)
        for diction in cursor:
            document = Url(diction.get('url'), diction.get('title'), diction.get('description'), diction.get('appearance'), diction.get('word in page'))

            #check if we have title
            if document.title != None:
                if word in document.title:
                    document.sco

            # if the url in the dictionary so we increase the field "count" (in Url class) by one
            if GruopWord(clean, word, document):
                if document.url in dictionaryRel.keys():
                    dictionaryRel.get(document.url).count+=1
                # else we create a new key and value(object from class Url in Url_Address.py)
                else:
                    dictionaryRel[document.url] = document
            else:
                if document.url in dictionaryPartRel.keys():
                    dictionaryPartRel.get(document.url).count+=1
                # else we create a new key and value(object from class Url in Url_Address.py)
                else:
                    dictionaryPartRel[document.url] = document

    return dictionaryRel, dictionaryPartRel


def Look_up_new(dictionaryObjectRel, dictionaryObjectPartRel, DictionaryRanks):
    storeResultRelat = {}
    storeResultPartRelat = {}
    for linkRel in dictionaryObjectRel:
        if linkRel in DictionaryRanks:
            list_temp = []
            list_temp.append(DictionaryRanks[linkRel])
            list_temp.append(dictionaryObjectRel[linkRel])
            storeResultRelat[linkRel] = list_temp
    for linkPartRel in dictionaryObjectPartRel:
        if linkPartRel in DictionaryRanks:
            list_temp = []
            list_temp.append(DictionaryRanks[linkPartRel])
            list_temp.append(dictionaryObjectPartRel[linkPartRel])
            storeResultPartRelat[linkPartRel] = list_temp

    SortedByRankRel = {k: v for k, v in sorted(storeResultRelat.items(), key=lambda item: item[1][0], reverse=True)}
    SortedByRankPartRel = {k: v for k, v in sorted(storeResultPartRelat.items(), key=lambda item: item[1][0], reverse=True)}
    print("rel: ", SortedByRankRel)
    print("part: ", SortedByRankPartRel)



    #The Algorithm

        #maybe, 'for' on the rel and condition if the [len of the list of the links]-1 >15
        #(15 for example,-1 because i put the runk of link in front of the list of all links)
        #so add to final dict and delete it from original and in the end(it does'nt really matter!)
        #print to screen everything that left in the original dict,
        #and the same on the partrel.
        #and we left with one big dict sorted like this:
        # FinalResult = {'topRelevant':[link,desc,title]............'leastRelevant':[link,desc,title]}

    # and i go to restroom




def Create_list(dictionary):

    New_list = []

    for key in dictionary.keys():
        New_list.append(dictionary.get(key))
    return New_list


def compute_ranks(graph):

    d=0.8
    numloops=10
    ranks={}
    npages=len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * ranks[node] / len(graph[node])
            newranks[page] = newrank
        ranks = newranks
    return ranks

final_graph = {}
graph = Get_Graph()
for node in graph:
    #print(node)
    final_graph[node.get("_id")] = node.get("children")
dictionary = SSearch("duckduckgo controlling")
obj = LSIModel(dictionary)
obj.Lsi_model()
#dictionaryRel, dictionaryPartRel = Search_Query("come anonym answer 273")
#ranks=compute_ranks(final_graph)
#print(dictionaryPartRel)
#Look_up_new(dictionaryRel,dictionaryPartRel,ranks)


#Look_up_new(dictionaryPartRel,ranks2)



