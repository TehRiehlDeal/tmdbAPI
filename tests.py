from tmdbAPI import TMDB, ShowNotFound, InvalidInput
from classes.search import CollectionNotFound, CompanyNotFound, KeywordNotFound, MovieNotFound, MultiNotFound, PersonNotFound, TVNotFound
import unittest
import sys
sys.path.append("..")

class SearchTest(unittest.TestCase):

    def setUp(self):
        self.t = TMDB()

    def tearDown(self):
        self.t.session.close()

    def collectionSearchTest(self):
        assert type(self.t.search.searchCollection("Thriller")) == dict

    def collectionErrorTest(self):
        with self.assertRaises(CollectionNotFound):
            self.t.search.searchCollection('TESTSETETS')

    def companySearchTest(self):
        assert type(self.t.search.searchCompany("Warner")) == dict

    def companyErrorTest(self):
        with self.assertRaises(CompanyNotFound):
            self.t.search.searchCompany('TESTSETETS')

    def keywordSearchTest(self):
        assert type(self.t.search.searchKeyword("Thriller")) == dict

    def keywordErrorTest(self):
        with self.assertRaises(KeywordNotFound):
            self.t.search.searchKeyword('TESTSETETS')

    def movieSearchTest(self):
        assert type(self.t.search.searchMovie("John Wick")) == dict

    def movieErrorTest(self):
        with self.assertRaises(MovieNotFound):
            self.t.search.searchMovie('TESTSETETS')

    def multiSearchTest(self):
        assert type(self.t.search.searchMulti("Bleach")) == dict

    def multiErrorTest(self):
        with self.assertRaises(MultiNotFound):
            self.t.search.searchMulti('TESTSETETS')

    def personSearchTest(self):
        assert type(self.t.search.searchPerson("Keanu Reeves")) == dict

    def personErrorTest(self):
        with self.assertRaises(PersonNotFound):
            self.t.search.searchPerson('TESTSETETS')

    def tvSearchTest(self):
        assert type(self.t.search.searchTV("Thriller")) == dict

    def tvErrorTest(self):
        with self.assertRaises(TVNotFound):
            self.t.search.searchTV('TESTSETETS')

if __name__ == "__main__":
    unittest.main()
