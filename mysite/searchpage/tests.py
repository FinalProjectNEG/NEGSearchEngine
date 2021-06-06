from django.test import TestCase

# Create your tests here.
from .DB import Get_Information
from .HelpFunctionScore import ScoreTime
from .Search import Search


class ModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_year_ago(self):
        dept = ScoreTime(time="date 1 Feb 2021")
        print(dept)
        self.assertEqual(dept, 5)

    def test_4year_ago(self):
        dept = ScoreTime(time="date 1 Feb 2018")
        print(dept)
        self.assertEqual(dept, 3)

    def test_21year_ago(self):
        dept = ScoreTime(time="date 1 Feb 2000")
        print(dept)
        self.assertEqual(dept, 2)

    def test_check_word_NOTin_DB(self):
        dept = Get_Information(word="p[p[p[")
        self.assertEqual(dept, None)

    def test_check_word_in_DB(self):
        dept = Get_Information(word="tower")
        self.assertNotEqual(dept,None)

    def test_found_searchquery(self):
        object_search = Search("covid-19")
        self.assertNotEqual(object_search,"not found")

    def test_found_searchquery_hebrew(self):
        object_search = Search("האח הגדול")
        self.assertNotEqual(object_search,"not found")

    def test_not_found_query(self):
        object_search = Search("sssssssssssssssssssssssssssssssssss")
        results = object_search.Start_search()
        self.assertEqual(results,"not found")

        