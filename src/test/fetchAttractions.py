import unittest
from trip_planner_app import TripPlannerApp, Attraction

class TestTripPlannerApp(unittest.TestCase):
    def setUp(self):
        self.app = TripPlannerApp('trip_planner.db')

    def test_get_attractions(self):
        attractions = self.app.get_attractions(1)  # Assuming 1 is a valid destination ID
        self.assertIsInstance(attractions, list)
        self.assertGreater(len(attractions), 0)
        self.assertIsInstance(attractions[0], Attraction)

if __name__ == '__main__':
    unittest.main()