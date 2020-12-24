from gensim import corpora
from gensim.models import LsiModel


class LSIModel:

    def __init__(self,dictionary):

        self.list_word=[]
        for key in dictionary:
            self.list_word.append(list(dictionary.get(key).dictionary_word.keys()))
        print(self.list_word[0])
        print(len(self.list_word[0]))
        self.number_of_topics = 7
        self.words = 10

    def prepare_corpus(self, doc_clean):
        """
        Input  : clean document
        Purpose: create term dictionary of our courpus and Converting list of documents (corpus) into Document Term Matrix
        Output : term dictionary and Document Term Matrix
        """
        # Creating the term dictionary of our courpus, where every unique term is assigned an index. dictionary = corpora.Dictionary(doc_clean)
        dictionary = corpora.Dictionary(doc_clean)
        # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
        # generate LDA model
        return dictionary, doc_term_matrix


    def make_Lsi_model(self):
        dictionary, doc_term_matrix = self.prepare_corpus(self.list_word)
        # generate LSA model
        lsamodel = LsiModel(doc_term_matrix, num_topics=self.number_of_topics, id2word=dictionary)  # train model
        print(lsamodel.print_topics(num_topics=self.number_of_topics, num_words=self.words))
        return lsamodel

    def Lsi_model(self):
        model = self.make_Lsi_model()
        print(model)
