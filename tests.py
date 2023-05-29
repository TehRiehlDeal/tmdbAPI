from tmdbAPI import TMDB, ShowNotFound, InvalidInput
from classes.search import CollectionNotFound, CompanyNotFound, KeywordNotFound, MovieNotFound, MultiNotFound, PersonNotFound, TVNotFound
import unittest
import sys
sys.path.append("..")

class TestSearch(unittest.TestCase):

    def setUp(self):
        self.t = TMDB()

    def tearDown(self):
        self.t.session.close()

    def testCollectionSearch(self):
        assert type(self.t.search.searchCollection("Action")) == dict

    def testCollectionError(self):
        with self.assertRaises(CollectionNotFound):
            self.t.search.searchCollection('TESTSETETS')

    def testCompanySearch(self):
        assert type(self.t.search.searchCompany("Warner")) == dict

    def testCompanyError(self):
        with self.assertRaises(CompanyNotFound):
            self.t.search.searchCompany('TESTSETETS')

    def testKeywordSearch(self):
        assert type(self.t.search.searchKeyword("Thriller")) == dict

    def testKeywordError(self):
        with self.assertRaises(KeywordNotFound):
            self.t.search.searchKeyword('TESTSETETS')

    def testMovieSearch(self):
        assert type(self.t.search.searchMovie("John Wick")) == dict

    def testMovieError(self):
        with self.assertRaises(MovieNotFound):
            self.t.search.searchMovie('TESTSETETS')

    def testMultiSearch(self):
        assert type(self.t.search.searchMulti("Bleach")) == dict

    def testMultiError(self):
        with self.assertRaises(MultiNotFound):
            self.t.search.searchMulti('TESTSETETS')

    def testPersonSearch(self):
        assert type(self.t.search.searchPerson("Keanu Reeves")) == dict

    def testPersonError(self):
        with self.assertRaises(PersonNotFound):
            self.t.search.searchPerson('TESTSETETS')

    def testTVSearch(self):
        assert type(self.t.search.searchTV("Thriller")) == dict

    def testTVError(self):
        with self.assertRaises(TVNotFound):
            self.t.search.searchTV('TESTSETETS')

if __name__ == "__main__":
    unittest.main()
