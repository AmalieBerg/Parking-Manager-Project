"""
Repository Pattern for Parking Lot Data Access
Provides persistence ignorance
FIXED: Proper encapsulation, auto-detection of slot types
"""

from typing import Optional, List, Tuple
from models import Vehicle, ElectricVehicle, ParkingSlot, ParkingLevel


class ParkingRepository:
    """
    Repository for managing parking lot data - implements Repository Pattern
    FIXED: No direct access to private attributes
    FIXED: Auto-detects slot type when removing
    FIXED: Global sequential slot numbering across all levels
    """
    
    def __init__(self):
        self._levels: List[ParkingLevel] = []
        self._next_slot_number: int = 1  # Global slot counter
    
    def create_level(self, level_number: int, regular_capacity: int, 
                    ev_capacity: int) -> ParkingLevel:
        """
        Create a new parking level with global sequential slot numbers
        Returns: (level, start_slot, end_slot)
        """
        start_slot = self._next_slot_number
        
        level = ParkingLevel(level_number, regular_capacity, ev_capacity, start_slot)
        self._levels.append(level)
        
        # Update global slot counter for next level
        self._next_slot_number += (regular_capacity + ev_capacity)
        
        return level
    
    def get_level(self, level_number: int) -> Optional[ParkingLevel]:
        """Get a level by its number"""
        for level in self._levels:
            if level.level_number == level_number:
                return level
        return None
    
    def find_available_slot(self, is_ev: bool) -> Optional[Tuple[ParkingLevel, ParkingSlot]]:
        """Find first available slot of specified type"""
        for level in self._levels:
            if is_ev:
                available_slots = level.get_available_ev_slots()
            else:
                available_slots = level.get_available_regular_slots()
            
            if available_slots:
                return (level, available_slots[0])
        return None
    
    def park_vehicle(self, vehicle: Vehicle) -> Optional[Tuple[ParkingLevel, ParkingSlot]]:
        """
        Park a vehicle in the first available slot
        Automatically determines slot type based on vehicle type
        """
        is_ev = isinstance(vehicle, ElectricVehicle)
        result = self.find_available_slot(is_ev)
        
        if result:
            level, slot = result
            # FIXED: Use public method instead of accessing _private
            actual_slot = level.find_slot_by_number(slot.slot_number)
            if actual_slot and actual_slot.park_vehicle(vehicle):
                return (level, actual_slot)
        return None
    
    def remove_vehicle(self, slot_number: int) -> Optional[Tuple[ParkingLevel, ParkingSlot, Vehicle]]:
        """
        Remove vehicle by slot number only
        FIXED: Auto-detects which level and slot type - no manual specification needed!
        Returns: (level, slot, vehicle) if found, None otherwise
        """
        for level in self._levels:
            slot = level.find_slot_by_number(slot_number)
            if slot and slot.is_occupied:
                vehicle = slot.remove_vehicle()
                return (level, slot, vehicle)
        return None
    
    def find_vehicle_by_regnum(self, regnum: str) -> Optional[Tuple[ParkingLevel, ParkingSlot, Vehicle]]:
        """Find a vehicle by registration number (searches all levels and slot types)"""
        for level in self._levels:
            for slot in level.get_all_slots():
                if slot.is_occupied and slot.vehicle.regnum == regnum:
                    return (level, slot, slot.vehicle)
        return None
    
    def find_vehicles_by_color(self, color: str) -> List[Tuple[ParkingLevel, ParkingSlot, Vehicle]]:
        """Find all vehicles of a given color"""
        results = []
        for level in self._levels:
            for slot in level.get_all_slots():
                if slot.is_occupied and slot.vehicle.color.lower() == color.lower():
                    results.append((level, slot, slot.vehicle))
        return results
    
    def get_all_parked_vehicles(self) -> List[Tuple[ParkingLevel, ParkingSlot, Vehicle]]:
        """Get all currently parked vehicles"""
        results = []
        for level in self._levels:
            for slot in level.get_occupied_regular_slots():
                results.append((level, slot, slot.vehicle))
            for slot in level.get_occupied_ev_slots():
                results.append((level, slot, slot.vehicle))
        return results
    
    def get_all_ev_vehicles(self) -> List[Tuple[ParkingLevel, ParkingSlot, ElectricVehicle]]:
        """Get all currently parked electric vehicles"""
        results = []
        for level in self._levels:
            for slot in level.get_occupied_ev_slots():
                if isinstance(slot.vehicle, ElectricVehicle):
                    results.append((level, slot, slot.vehicle))
        return results
    
    def update_ev_charge(self, slot_number: int, new_charge: int) -> bool:
        """
        Update the charge level of an electric vehicle
        Returns True if successful, False if slot not found or not an EV
        """
        for level in self._levels:
            slot = level.find_slot_by_number(slot_number)
            if slot and slot.is_occupied and isinstance(slot.vehicle, ElectricVehicle):
                slot.vehicle.charge = new_charge
                return True
        return False
