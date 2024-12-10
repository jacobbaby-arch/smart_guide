import unittest
from trip_planner_app import TripPlannerApp, Country

class TestTripPlannerApp(unittest.TestCase):
    def setUp(self):
        self.app = TripPlannerApp('trip_planner.db')

    def test_get_countries(self):
        countries = self.app.get_countries(1)  # Assuming 1 is a valid continent ID
        self.assertIsInstance(countries, list)
        self.assertGreater(len(countries), 0)
        self.assertIsInstance(countries[0], Country)

if __name__ == '__main__':
    unittest.main()