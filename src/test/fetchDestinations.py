import unittest
from trip_planner_app import TripPlannerApp, Destination

class TestTripPlannerApp(unittest.TestCase):
    def setUp(self):
        self.app = TripPlannerApp('trip_planner.db')

    def test_get_destinations(self):
        destinations = self.app.get_destinations(1)  # Assuming 1 is a valid country ID
        self.assertIsInstance(destinations, list)
        self.assertGreater(len(destinations), 0)
        self.assertIsInstance(destinations[0], Destination)

if __name__ == '__main__':
    unittest.main()