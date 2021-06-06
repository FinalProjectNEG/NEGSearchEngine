from datetime import date, datetime
from sqlite3.dbapi2 import Date

import nltk as nltk
import numpy as np
from nltk.tokenize.regexp import WordPunctTokenizer
from .DB import Get_Information, listDB
from .Page_Rank import Page_Rank
from .Url_Address import Url
import math
from nltk.stem.porter import PorterStemmer

stopwords = nltk.corpus.stopwords.words('english')
# for tokenize the text from the page
tokenizer = WordPunctTokenizer()
stemmer = PorterStemmer()

class Search:


    def __init__(self,query):
        self.query = query

    def GruopWord(self, listtword, word, obj):
        # copy of list of words
        list_temp = listtword.copy()
        if word in listtword:
            list_temp.remove(word)

        for word1 in list_temp:
            if(word1 in obj.dictionary_word.keys()):
                return True

        return False

    def SSearch(self, query):
        # do tokenize to the query, split_query is list
        tokens = tokenizer.tokenize(query)
        dictionary={}

        if len(tokens) > 1:
            # remove stopwords that not include DB
            clean = [token.lower() for token in tokens if token.lower() not in stopwords and len(token) > 2]
        else:
            clean = tokens.copy()
        final = [stemmer.stem(word) for word in clean]
        final_list = listDB(final)
        print("final: ",final)
        for word in final_list:
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
                per_score_title = float(50 / len(temp_title))
                final_score_title = math.floor(true_title * per_score_title)
                dictionary.get(key).score += final_score_title


            if dictionary.get(key).description != None:
                temp_description = dictionary.get(key).appear_word_description
                true_description = temp_description.count(True)
                per_score_description = 7 / len(temp_description)
                final_score_description = math.floor(true_description * per_score_description)
                dictionary.get(key).score += final_score_description

        return dictionary, final

    def Start_search(self):

        dictionary, final = self.SSearch(self.query)
        if len(dictionary) == 0:
            return "not found"
        object_page_rank = Page_Rank(dictionary, final)
        result_ranking = object_page_rank.Start_Ranking()
        return result_ranking

