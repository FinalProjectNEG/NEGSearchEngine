from datetime import date
from .DB import Get_Graph
from .Tf_Idf import Tf_Idf

dict_month = {"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}

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
            print(self.dictionary.get(key).score)
            self.dictionary.get(key).score += ranks.get(key)
            print(self.dictionary.get(key).score)
        print("ranks: ", ranks)

    def checkTime(self):

        for key in self.dictionary:
            time = self.dictionary.get(key).time
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
                    self.dictionary.get(key).score += 5
                elif (year_ago_10 < date_page < year_ago_1):
                    self.dictionary.get(key).score += 3
                elif (date_page < year_ago_10):
                    self.dictionary.get(key).score += 2

    def Create_final_graph(self):
        graph = Get_Graph()
        for node in graph:
            # print(node)
            self.final_graph[node.get("_id")] = node.get("children")

    def Start_Ranking(self):
        self.Create_final_graph()
        self.checkTime()
        object_Tf_idf = Tf_Idf(self.dictionary, self.query)
        self.dictionary = object_Tf_idf.Start_Tf_Idf()
        self.compute_ranks()
        sort_dictionary = {k: v for k, v in sorted(self.dictionary.items(), key=lambda item: item[1].score, reverse=True)}
        return sort_dictionary