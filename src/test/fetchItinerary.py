import unittest
from trip_planner_app import TripPlannerApp, Itinerary

class TestTripPlannerApp(unittest.TestCase):
    def setUp(self):
        self.app = TripPlannerApp('trip_planner.db')

    def test_get_itinerary(self):
        itinerary = self.app.get_itinerary(1)  # Assuming 1 is a valid destination ID
        self.assertIsInstance(itinerary, list)
        self.assertGreater(len(itinerary), 0)
        self.assertIsInstance(itinerary[0], Itinerary)

if __name__ == '__main__':
    unittest.main()