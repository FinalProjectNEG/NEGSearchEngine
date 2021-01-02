import math

import nltk
import numpy as np


class Tf_Idf:

    def __init__(self, dictionary, final):
        self.dictionary = dictionary
        self.query = final

    #calculate the query vector and return vector Q
    def gen_vector(self, tokens, total_vocab):
        Q = np.zeros((len(total_vocab)))

        counter = nltk.Counter(tokens)
        words_count = len(tokens)

        query_weights = {}
        len_dict = len(self.dictionary.keys())
        for token in np.unique(tokens):

            tf = counter[token] / words_count
            noDocsWordAppers = self.Count_documents(token)
            df = noDocsWordAppers / len_dict
            idf = math.log((len_dict + 1) / (df + 1))

            try:

                ind = total_vocab.index(token)
                Q[ind] = tf * idf

            except:
                pass
        return Q

    #calculate the Cosine Similarity
    def cosine_sim(self, a, b):

        if(np.linalg.norm(a)*np.linalg.norm(b) == 0):
            cos_sim = 0
        else:
            cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
        return cos_sim

    def cosine_similarity(self, D, total_vocab, list_of_docs_byNum):
        print("Cosine Similarity")
        tokens = self.query

        print("\nQuery:", self.query)
        print("")

        d_cosines = []

        query_vector = self.gen_vector(tokens, total_vocab)

        for d in D:
            d_cosines.append(self.cosine_sim(query_vector, d))
        # print("d_cos = ",d_cosines)
        out = np.array(d_cosines).argsort()
        # print(out)
        for number in out:
            link = list_of_docs_byNum.get(number)
            self.dictionary.get(link).score += d_cosines[number]

    def Convert_Vectorize(self, tf_idf):
        len_dict = len(self.dictionary.keys())
        total_vocab = self.Calculate_DF()
        total_vocab_size = len(total_vocab)
        D = np.zeros((len_dict, total_vocab_size))
        for i in tf_idf:
            try:

                ind = total_vocab.index(i[1])
                D[i[0]][ind] = tf_idf[i]
            except:
                pass
        return D, total_vocab

    def Calculate_DF(self):
        list_df = []

        for key in self.dictionary:
            list_df.extend(list(self.dictionary.get(key).dictionary_word.keys()))
        return list(np.unique(list_df))

    def Tf_Idf_calc(self):
        tf_idf = {}
        len_dict = len(self.dictionary.keys())
        dic_total_words = {}
        noOfDoc = 0
        list_of_docs_by_number = {}
        for key in self.dictionary:
            # dictionary of word in body {"word": [count, tf]}
            tokens = self.dictionary.get(key).dictionary_word
            for token in tokens:
                tf = tokens.get(token)[1]
                # function recieve "word"
                noDocsWordAppers = self.Count_documents(token)
                df = noDocsWordAppers / len_dict
                idf = np.log(len_dict / (df + 1))
                tf_idf[noOfDoc, token] = tf * idf
            list_of_docs_by_number[noOfDoc] = key
            noOfDoc += 1

        # {"[url,word]": num, ....}
        return tf_idf, list_of_docs_by_number

    def Count_documents(self, word):
        count_element = 0
        for key in self.dictionary:

            if word in self.dictionary.get(key).dictionary_word.keys():
                count_element += 1

        return count_element

    def Start_Tf_Idf(self):
        tf_idf, list_of_docs_byNum = self.Tf_Idf_calc()
        D, total_vocab = self.Convert_Vectorize(tf_idf)
        self.cosine_similarity( D, total_vocab, list_of_docs_byNum)
        return self.dictionary
