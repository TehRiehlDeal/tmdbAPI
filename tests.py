from tmdbAPI import TMDB, ShowNotFound, InvalidInput
import unittest
import sys
sys.path.append("..")


class TestGetShow(unittest.TestCase):

    def setUp(self):
        self.t = TMDB()

    def tearDown(self):
        self.t.session.close()

    # Test to see if its working correctly
    def testA(self):
        assert type(self.t.getShow("Mythbusters")) == dict

    # Test to see if showNotFound is raised correctly
    def testB(self):
        # self.failUnlessRaises(showNotFound, self.t.getShow("TETSTSETSTSETT"))
        with self.assertRaises(ShowNotFound):
            self.t.getShow('TESTSETETS')

    # Tests to see if invalidInput is raised correctly
    def testC(self):
        with self.assertRaises(InvalidInput):
            self.t.getShow(-1)

    def testD(self):
        with self.assertRaises(InvalidInput):
            self.t.getShow({'test': "test"})

    def testE(self):
        with self.assertRaises(InvalidInput):
            assert self.t.getShow(["a", "b", "c"])

    # Tests to see if a show can be successfully found based on an alias.
    # In this case the alias is To aru Majutsu no Index, but it is being matched
    # by string likeness.
    def testF(self):
        assert type(self.t.getShow("Toaru Majutsu no Index")) == dict

if __name__ == "__main__":
    unittest.main()
