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
class CarparkManager(CarparkSensorListener, CarparkDataProvider):
    """Manages carpark operations and state.
    
    Implements both CarparkSensorListener (for receiving sensor events)
    and CarparkDataProvider (for supplying display data).
    """
    
    CONFIG_FILE = "smartpark/config.json"
    
    def __init__(self, config_file=None):
        """Initialize CarparkManager from configuration file."""
        if config_file is None:
            config_file = CarparkManager.CONFIG_FILE
        
        config = parse_config(config_file)
        self.location = config.get("location", "Unknown")
        self.total_spaces = int(config.get("total-spaces", 100))
        self._available_spaces = self.total_spaces
        self._temperature = 0
        self.cars = {}
        self.log_file = config.get("log_file", "carpark.log")
        
        self._log_event("INIT", f"Carpark initialized: {self.location}")
    
    #CarparkDataProvider Properties 
    
    @property
    def available_spaces(self):
        """Return current available parking spaces."""
        return self._available_spaces
    
    @property
    def temperature(self):
        """Return current temperature reading."""
        return self._temperature
    
    @property
    def current_time(self):
        """Return current time as struct_time for display."""
        return time.localtime()
    
    #CarparkSensorListener Methods
    
    def incoming_car(self, license_plate):
        """Handle a car entering the carpark."""
        if self._available_spaces > 0:
            self._available_spaces -= 1
            car = Car(license_plate)
            self.cars[license_plate] = car
            self._log_event("ENTRY", f"{license_plate} entered")
    
    def outgoing_car(self, license_plate):
        """Handle a car exiting the carpark."""
        if license_plate in self.cars:
            car = self.cars.pop(license_plate)
            car.exit_time = datetime.now()
            self._available_spaces = min(self._available_spaces + 1, self.total_spaces)
            self._log_event("EXIT", f"{license_plate} exited")
    
    def temperature_reading(self, reading):
        """Update temperature from sensor reading."""
        self._temperature = int(reading)

    # Logging method
    def _log_event(self, event_type, message):
        """Write event to log file."""
        timestamp = datetime.now().isoformat()
        with open(self.log_file, 'a') as f:
            f.write(f"{timestamp} | {event_type} | {message}\n")    

class Car:
    """Represents a car in the carpark system.
    
    Attributes:
        license_plate (str): The vehicle's license plate number.
        entry_time (datetime): When the car entered the carpark.
        exit_time (datetime | None): When the car exited, or None if parked.
    """
    
    def __init__(self, license_plate: str):
        """Initialize a Car instance.
        
        Args:
            license_plate: The vehicle's license plate identifier.
        """
        self.license_plate = license_plate
        self.entry_time = datetime.now()
        self.exit_time = None