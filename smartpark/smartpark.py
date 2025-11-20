from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
from config_parser import parse_config
import time
from datetime import datetime

'''
    TODO: 
    - make your own module, or rename this one. Yours won't be a mock-up, so "mocks" is a bad name here.
    - Read your configuration from a file. 
    - Write entries to a log file when something happens.
    - The "display" should update instantly when something happens
    - Make a "Car" class to contain information about cars:
        * License plate number. You can use this as an identifier
        * Entry time
        * Exit time
    - The manager class should record all activity. This includes:
        * Cars arriving
        * Cars departing
        * Temperature measurements.
    - The manager class should provide informtaion to potential customers:
        * The current time (optional)
        * The number of bays available
        * The current temperature
    
'''
class MockCarparkManager(CarparkSensorListener,CarparkDataProvider):
    #constant, for where to get the configuration data
    CONFIG_FILE = "carpark_config.txt"

def __init__(self, config_file="samples_and_snippets/config.json"):
    """Initialize manager from config file."""
    config = parse_config(config_file)
    self.location = config['location']
    self.total_spaces = config['total-spaces']
    self.cars = {}
    self._temperature = 25.0
    self.log_file = "carpark.log"
    self._log("SYSTEM", f"Carpark initialized: {self.location}")

def _log(self, event_type, message):
    """Write event to log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(self.log_file, 'a') as f:
        f.write(f"[{timestamp}] {event_type}: {message}\n")

    @property
    def available_spaces(self):
     """Return available spaces (never negative)."""
    spaces = self.total_spaces - len(self.cars)
    return max(0, spaces)

    @property
    def temperature(self):
     """Return current temperature."""
    return self._temperature

    @property
    def current_time(self):
        return time.localtime()

    def incoming_car(self, license_plate):
     """Handle car entering carpark."""
    if not license_plate:
        return
    plate = license_plate.upper().strip()
    # Check if already parked
    if plate in self.cars:
        self._log("WARNING", f"Car {plate} already parked")
        return
    # Check if full
    if self.available_spaces <= 0:
        self._log("WARNING", f"Car {plate} denied - carpark full")
        return
    # Add car
    self.cars[plate] = Car(plate)
    self._log("ENTRY", f"Car {plate} entered | Available: {self.available_spaces}")
    print(f"Car {plate} entered. Available: {self.available_spaces}")


    def outgoing_car(self, license_plate):
     """Handle car leaving carpark."""
    if not license_plate:
        return
    plate = license_plate.upper().strip()
    # Check if registered
    if plate not in self.cars:
        self._log("WARNING", f"Car {plate} not found")
        return
    # Remove car
    del self.cars[plate]
    self._log("EXIT", f"Car {plate} exited | Available: {self.available_spaces}")
    print(f"Car {plate} exited. Available: {self.available_spaces}")

    def temperature_reading(self, reading):
     """Update temperature."""
    self._temperature = reading
    self._log("TEMP", f"Temperature: {reading}°C")

class Car:
    """
    Represents a car in the carpark.
    Attributes:
        license_plate (str): Vehicle license plate
        entry_time (datetime): When car entered
    """
    def __init__(self, license_plate):
        """Initialize car with license plate."""
        self.license_plate = license_plate.upper().strip()
        self.entry_time = datetime.now()        