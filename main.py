from datetime import date, datetime
from sqlite3.dbapi2 import Date

import nltk as nltk
import numpy as np
from nltk.tokenize.regexp import WordPunctTokenizer
from DB import Get_Information, Get_Graph
from Url_Address import Url
from LSIModel import LSIModel
import math
from nltk.stem.porter import PorterStemmer

dict_month = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}

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
                           diction.get('appearance'), diction.get('word in page'), diction.get('date modified'))

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

    return dictionary, final


def checkTime(dictionary):

    for key in dictionary:
        time = dictionary.get(key).time
        if time != None:
            today = date.today()
            date_information = time.split()
            day = date_information[1]
            month = date_information[2]
            year = date_information[3]

            date_page = date(year,dict_month[month],day)
            year_ago_1 = date(today.year-1,today.month,today.day)
            year_ago_10 = date(today.year-10,today.month,today.day)
            date_today = date(today.year,today.month,today.day)

            if(year_ago_1 < date_page < date_today):
                dictionary.get(key).score += 5
            elif (year_ago_10 < date_page < year_ago_1):
                dictionary.get(key).score += 3
            elif (date_page < year_ago_10):
                dictionary.get(key).score += 2
    return dictionary

def Count_documents(word, dictionary):

    #list_obj = []
    count_element = 0
    for key in dictionary:

        #print("key == ",dictionary.get(key).dictionary_word.keys())
        #print(dictionary.get(key).dictionary_word.keys())
        if word in dictionary.get(key).dictionary_word.keys():
            count_element+=1
            #list_obj.append(dictionary.get(key))
            #if word=="learn":
            #    print(list_obj)

    return count_element



def Tf_Idf(dictionary):
    tf_idf = {}
    len_dict = len(dictionary.keys())
    dic_total_words = {}
    noOfDoc=0
    list_of_docs_by_number={}
    for key in dictionary:
        #dictionary of word in body {"word": [count, tf]}
        tokens = dictionary.get(key).dictionary_word
        for token in tokens:
            tf = tokens.get(token)[1]
            # function recieve "word"
            noDocsWordAppers = Count_documents(token, dictionary)
            df = noDocsWordAppers/len_dict
            idf = np.log(len_dict / (df + 1))
            tf_idf[noOfDoc, token] = tf * idf
        list_of_docs_by_number[noOfDoc]=key
        noOfDoc+=1

    # {"[url,word]": num, ....}
    return tf_idf,list_of_docs_by_number


def Calculate_DF(dictionary):
    list_df = []

    for key in dictionary:
        list_df.extend(list(dictionary.get(key).dictionary_word.keys()))
    return list(np.unique(list_df))


def Convert_Vectorize(tf_idf,list_docs_byNum, dictionary):
    len_dict = len(dictionary.keys())
    total_vocab = Calculate_DF(dictionary)
    total_vocab_size = len(total_vocab)
    D = np.zeros((len_dict, total_vocab_size))
    for i in tf_idf:
        try:
            #print("i[0] = ", i[0])
            #print("i = ", i)
            ind = total_vocab.index(i[1])
            D[i[0]][ind] = tf_idf[i]
            #print("doc:",list_docs_byNum[i[0]])
        except:
            pass
    #print("tf_idf: ",tf_idf)
    return D, total_vocab


def gen_vector(tokens, total_vocab, dictionary):
    Q = np.zeros((len(total_vocab)))

    counter = nltk.Counter(tokens)
    words_count = len(tokens)

    query_weights = {}
    len_dict = len(dictionary.keys())
    for token in np.unique(tokens):

        tf = counter[token] / words_count
        noDocsWordAppers = Count_documents(token, dictionary)
        df = noDocsWordAppers/len_dict
        idf = math.log((len_dict + 1) / (df + 1))
        # print("token = ", token)
        # print("tf = ",tf)
        # print("noDoc = ", noDocsWordAppers)
        # print("df = ",df)
        # print("idf = ", idf)

        try:
            # print(total_vocab)
            # print("ttt = ",token)
            ind = total_vocab.index(token)
            # print("ind", ind)
            Q[ind] = tf * idf
            # print("ans: ", tf*idf)
        except:
            pass
    return Q


def cosine_sim(a, b):
    #print("a= ",a," b= ",b)
    # print("1: ",np.linalg.norm(a))
    # print("2: ",np.linalg.norm(b))
    #print("3: ", np.dot(a, b))
    if(np.linalg.norm(a)*np.linalg.norm(b) == 0):
        cos_sim = 0
    else:
        cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim


def cosine_similarity(k, query, D, final, total_vocab, dictionary, list_of_docs_byNum):
    print("Cosine Similarity")
    tokens = final

    print("\nQuery:", query)
    print("")
    #print(tokens)

    d_cosines = []

    query_vector = gen_vector(tokens, total_vocab,dictionary)

    for d in D:
        d_cosines.append(cosine_sim(query_vector, d))
    #print("d_cos = ",d_cosines)
    out = np.array(d_cosines).argsort()
    #print(out)
    for number in out:
        link = list_of_docs_byNum.get(number)
        dictionary.get(link).score += d_cosines[number]
        # print("link: ", link)
        # print("number: ",number)
        # print("score: ",dictionary.get(link).score)
    return dictionary



def matching_score(tf_idf, query):
    query_weights = {}
    for key in tf_idf:
        if key[1] in query:
            query_weights[key[0]] += tf_idf[key]


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
    for key in ranks:
        print(dictionary.get(key).score)
        dictionary.get(key).score += ranks.get(key)
        print(dictionary.get(key).score)
    print("ranks: ",ranks)
    return dictionary

final_graph = {}
graph = Get_Graph()
for node in graph:
    #print(node)
    final_graph[node.get("_id")] = node.get("children")
query = "controlling duckduckgo"
dictionary, final = SSearch(query)
dictionary = checkTime(dictionary)
tf_idf,list_of_docs_byNum = Tf_Idf(dictionary)
D, total_vocab = Convert_Vectorize(tf_idf,list(list_of_docs_byNum.keys()), dictionary)
dictionary = cosine_similarity(10, query, D, final,total_vocab,dictionary, list_of_docs_byNum)
dictionary = compute_ranks(final_graph)
#print(dictionaryPartRel)
#Look_up_new(dictionaryRel,dictionaryPartRel,ranks)


#Look_up_new(dictionaryPartRel,ranks2)



