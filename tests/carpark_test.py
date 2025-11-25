"""Unit tests for CarparkManager class."""
import unittest
import os
import sys
from pathlib import Path

cwd = Path(os.path.dirname(__file__))
parent = str(cwd.parent)
sys.path.append(parent + "/smartpark")

from carpark_manager import CarparkManager, Car


class TestCarparkManager(unittest.TestCase):
    """Test cases for CarparkManager."""
    
    def setUp(self):
        """Create test config file."""
        self.test_config = "test_config.json"
        with open(self.test_config, 'w') as f:
            f.write('{"CarParks": [{"location": "Test", "total-spaces": 5}]}')
    
    def tearDown(self):
        """Clean up test files."""
        for f in [self.test_config, "carpark.log"]:
            if os.path.exists(f):
                os.remove(f)
    
    def test_available_spaces_never_negative(self):
        """Verify available spaces cannot go below zero."""
        manager = CarparkManager(self.test_config)
        for i in range(10):
            manager.incoming_car(f"CAR{i}")
        self.assertEqual(manager.available_spaces, 0)
    
    def test_unknown_car_exit_no_increment(self):
        """Verify unknown car exit does not free a space."""
        manager = CarparkManager(self.test_config)
        initial = manager.available_spaces
        manager.outgoing_car("UNKNOWN")
        self.assertEqual(manager.available_spaces, initial)


if __name__ == "__main__":
    unittest.main()