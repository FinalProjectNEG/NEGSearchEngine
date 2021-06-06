from .DB import Get_Graph
from .HelpFunctionScore import ScoreTime
from .Tf_Idf import Tf_Idf


class Page_Rank:

    def __init__(self,dictionary,query):
        self.dictionary = dictionary
        self.final_graph = {}
        self.query = query

    def compute_ranks(self):

        d = 0.8
        numloops = 10
        ranks = {}
        npages = len(self.final_graph)
        for page in self.final_graph:
            ranks[page] = 1.0 / npages
        for i in range(0, numloops):
            newranks = {}
            for page in self.final_graph:
                newrank = (1 - d) / npages
                for node in self.final_graph:
                    if page in self.final_graph[node]:
                        newrank = newrank + d * ranks[node] / len(self.final_graph[node])
                newranks[page] = newrank
            ranks = newranks
        for key in ranks:
            print("ooooooo "+str(key))
            self.dictionary.get(key).score += ranks.get(key)
           # print(self.dictionary.get(key).score)
        #print("ranks: ", ranks)


    def checkTime(self):

        for key in self.dictionary:
            time = self.dictionary.get(key).time
            self.dictionary.get(key).score += ScoreTime(time)


    def Create_final_graph(self):
        graph = Get_Graph()
        for node in graph:
            # print(node)
            if(node.get("_id") in self.dictionary):
                self.final_graph[node.get("_id")] = node.get("children")

    def Start_Ranking(self):
        self.Create_final_graph()
        self.checkTime()
        object_Tf_idf = Tf_Idf(self.dictionary, self.query)
        self.dictionary = object_Tf_idf.Start_Tf_Idf()
        self.compute_ranks()
        sort_dictionary = {k: v for k, v in sorted(self.dictionary.items(), key=lambda item: item[1].score, reverse=True)}
        return sort_dictionary