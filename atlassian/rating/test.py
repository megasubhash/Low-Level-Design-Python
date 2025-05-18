from ast import Assert
import unittest

from rating import RatingManager
class TestRating(unittest.TestCase):

    def setUp(self):
        self.rating_manager = RatingManager()
        self.rating_manager.give_rating("Subhash", 10)
        self.rating_manager.give_rating("Subhash", 10)
        self.rating_manager.give_rating("Sahu", 10)
        pass
    

    def test_rating(self):
        res = self.rating_manager.get_ratings()
        self.assertEqual(res[0][0], "Subhash")
        


if __name__ == "__main__":
    unittest.main()