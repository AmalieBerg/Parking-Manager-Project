"""
Domain Models for Parking Lot Manager
Implements proper inheritance and encapsulation
FIXED: Sequential slot numbering, proper encapsulation
"""

from abc import ABC, abstractmethod
from typing import Optional
from enum import Enum


class VehicleType(Enum):
    """Enum for vehicle types - replaces magic strings"""
    CAR = "Car"
    MOTORCYCLE = "Motorcycle" 
    ELECTRIC_CAR = "Electric Car"
    ELECTRIC_BIKE = "Electric Bike"


class Vehicle(ABC):
    """Base Vehicle class with proper encapsulation"""
    
    def __init__(self, regnum: str, make: str, model: str, color: str):
        self._regnum = regnum
        self._make = make
        self._model = model
        self._color = color
    
    @property
    def regnum(self) -> str:
        return self._regnum
    
    @property
    def make(self) -> str:
        return self._make
    
    @property
    def model(self) -> str:
        return self._model
    
    @property
    def color(self) -> str:
        return self._color
    
    @abstractmethod
    def get_type(self) -> VehicleType:
        """Return the vehicle type"""
        pass
    
    def is_electric(self) -> bool:
        """Check if vehicle is electric"""
        return isinstance(self, ElectricVehicle)
    
    def __str__(self) -> str:
        return f"{self.get_type().value}: {self.make} {self.model} ({self.color}) - {self.regnum}"


class Car(Vehicle):
    """Regular car"""
    def __init__(self, regnum: str, make: str, model: str, color: str):
        super().__init__(regnum, make, model, color)
    
    def get_type(self) -> VehicleType:
        return VehicleType.CAR


class Motorcycle(Vehicle):
    """Regular motorcycle"""
    def __init__(self, regnum: str, make: str, model: str, color: str):
        super().__init__(regnum, make, model, color)
    
    def get_type(self) -> VehicleType:
        return VehicleType.MOTORCYCLE


class ElectricVehicle(Vehicle):
    """Base class for electric vehicles with charge management"""
    
    def __init__(self, regnum: str, make: str, model: str, color: str, 
                 initial_charge: int = 0):
        super().__init__(regnum, make, model, color)
        self._charge = initial_charge
    
    @property
    def charge(self) -> int:
        return self._charge
    
    @charge.setter
    def charge(self, value: int):
        if not 0 <= value <= 100:
            raise ValueError("Charge must be between 0 and 100")
        self._charge = value


class ElectricCar(ElectricVehicle):
    """Electric car - proper inheritance using super()"""
    
    def __init__(self, regnum: str, make: str, model: str, color: str, 
                 initial_charge: int = 0):
        super().__init__(regnum, make, model, color, initial_charge)
    
    def get_type(self) -> VehicleType:
        return VehicleType.ELECTRIC_CAR


class ElectricBike(ElectricVehicle):
    """Electric motorcycle - proper inheritance using super()"""
    
    def __init__(self, regnum: str, make: str, model: str, color: str, 
                 initial_charge: int = 0):
        super().__init__(regnum, make, model, color, initial_charge)
    
    def get_type(self) -> VehicleType:
        return VehicleType.ELECTRIC_BIKE


class ParkingSlot:
    """Represents a single parking slot"""
    
    def __init__(self, slot_number: int, is_ev_slot: bool = False):
        self._slot_number = slot_number
        self._is_ev_slot = is_ev_slot
        self._vehicle: Optional[Vehicle] = None
    
    @property
    def slot_number(self) -> int:
        return self._slot_number
    
    @property
    def is_ev_slot(self) -> bool:
        return self._is_ev_slot
    
    @property
    def vehicle(self) -> Optional[Vehicle]:
        return self._vehicle
    
    @property
    def is_occupied(self) -> bool:
        return self._vehicle is not None
    
    @property
    def is_available(self) -> bool:
        return self._vehicle is None
    
    def park_vehicle(self, vehicle: Vehicle) -> bool:
        """Park a vehicle in this slot"""
        if self.is_occupied:
            return False
        if self.is_ev_slot and not isinstance(vehicle, ElectricVehicle):
            return False
        self._vehicle = vehicle
        return True
    
    def remove_vehicle(self) -> Optional[Vehicle]:
        """Remove and return the parked vehicle"""
        vehicle = self._vehicle
        self._vehicle = None
        return vehicle


class ParkingLevel:
    """
    Represents a single parking level/floor
    FIXED: Sequential slot numbering across all slot types
    FIXED: Public methods for slot access (proper encapsulation)
    FIXED: Global sequential numbering across all levels
    """
    
    def __init__(self, level_number: int, regular_capacity: int, ev_capacity: int, 
                 start_slot_number: int = 1):
        self._level_number = level_number
        self._regular_capacity = regular_capacity
        self._ev_capacity = ev_capacity
        self._start_slot_number = start_slot_number
        
        # FIXED: Global sequential numbering
        # Regular slots: start_slot_number to (start_slot_number + regular_capacity - 1)
        # EV slots: (start_slot_number + regular_capacity) to (start_slot_number + regular_capacity + ev_capacity - 1)
        self._regular_slots: list[ParkingSlot] = [
            ParkingSlot(start_slot_number + i, is_ev_slot=False) 
            for i in range(regular_capacity)
        ]
        
        self._ev_slots: list[ParkingSlot] = [
            ParkingSlot(start_slot_number + regular_capacity + i, is_ev_slot=True) 
            for i in range(ev_capacity)
        ]
    
    @property
    def level_number(self) -> int:
        return self._level_number
    
    @property
    def regular_capacity(self) -> int:
        return self._regular_capacity
    
    @property
    def ev_capacity(self) -> int:
        return self._ev_capacity
    
    def get_slot_range(self) -> tuple[int, int]:
        """Get the range of slot numbers for this level (start, end inclusive)"""
        start = self._start_slot_number
        end = self._start_slot_number + self._regular_capacity + self._ev_capacity - 1
        return (start, end)
    
    def get_regular_slot_range(self) -> tuple[int, int]:
        """Get the range of regular slot numbers (start, end inclusive)"""
        start = self._start_slot_number
        end = self._start_slot_number + self._regular_capacity - 1
        return (start, end)
    
    def get_ev_slot_range(self) -> tuple[int, int]:
        """Get the range of EV slot numbers (start, end inclusive)"""
        start = self._start_slot_number + self._regular_capacity
        end = self._start_slot_number + self._regular_capacity + self._ev_capacity - 1
        return (start, end)
    
    def get_available_regular_slots(self) -> list[ParkingSlot]:
        """Get all available regular slots"""
        return [slot for slot in self._regular_slots if slot.is_available]
    
    def get_available_ev_slots(self) -> list[ParkingSlot]:
        """Get all available EV slots"""
        return [slot for slot in self._ev_slots if slot.is_available]
    
    def get_occupied_regular_slots(self) -> list[ParkingSlot]:
        """Get all occupied regular slots"""
        return [slot for slot in self._regular_slots if slot.is_occupied]
    
    def get_occupied_ev_slots(self) -> list[ParkingSlot]:
        """Get all occupied EV slots"""
        return [slot for slot in self._ev_slots if slot.is_occupied]
    
    def get_all_slots(self) -> list[ParkingSlot]:
        """Get all slots (regular + EV)"""
        return self._regular_slots + self._ev_slots
    
    def find_slot_by_number(self, slot_number: int) -> Optional[ParkingSlot]:
        """
        Find a slot by its number (searches both regular and EV slots)
        FIXED: Proper encapsulation - public method for slot access
        """
        for slot in self._regular_slots + self._ev_slots:
            if slot.slot_number == slot_number:
                return slot
        return None
