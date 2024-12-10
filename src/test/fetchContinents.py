import unittest
from trip_planner_app import TripPlannerApp, Continent

class TestTripPlannerApp(unittest.TestCase):
    def setUp(self):
        self.app = TripPlannerApp('trip_planner.db')

    def test_get_continents(self):
        continents = self.app.get_continents()
        self.assertIsInstance(continents, list)
        self.assertGreater(len(continents), 0)
        self.assertIsInstance(continents[0], Continent)

if __name__ == '__main__':
    unittest.main()