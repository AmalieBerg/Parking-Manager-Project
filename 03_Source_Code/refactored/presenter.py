"""
Presenter Layer - implements MVP Pattern
Mediates between Model (business logic) and View (GUI)
FIXED: Uses VehicleType enum, simplified remove, charge management
"""

from typing import Optional, List
from repository import ParkingRepository
from vehicle_factory import VehicleFactory
from models import Vehicle, ElectricVehicle, VehicleType


class ParkingPresenter:
    """
    Presenter in MVP pattern
    - Contains business logic
    - Mediates between View and Model
    - No direct GUI dependencies
    FIXED: Simplified interfaces, better validation
    """
    
    def __init__(self):
        self._repository = ParkingRepository()
    
    def create_parking_lot(self, regular_capacity: int, ev_capacity: int, 
                          level_number: int) -> str:
        """
        Create a new parking level with global sequential slot numbering
        FIXED: Better validation (zero capacity not allowed)
        FIXED: Shows global slot number ranges
        Returns: Success message
        """
        try:
            if regular_capacity <= 0 or ev_capacity <= 0:
                return "Error: Capacity must be greater than zero"
            
            level = self._repository.create_level(level_number, regular_capacity, ev_capacity)
            
            # Get the actual slot number ranges from the level
            regular_start, regular_end = level.get_regular_slot_range()
            ev_start, ev_end = level.get_ev_slot_range()
            
            return (f"Created parking lot with {regular_capacity} regular slots "
                   f"(#{regular_start}-{regular_end}) and {ev_capacity} EV slots "
                   f"(#{ev_start}-{ev_end}) on level {level_number}")
        
        except Exception as e:
            return f"Error creating parking lot: {str(e)}"
    
    def park_vehicle(self, regnum: str, make: str, model: str, color: str, 
                    vehicle_type: VehicleType, initial_charge: int = 0) -> str:
        """
        Park a vehicle
        FIXED: Uses VehicleType enum instead of booleans
        FIXED: Accepts initial_charge for electric vehicles
        Returns: Success/failure message
        """
        try:
            # Validate inputs
            if not all([regnum, make, model, color]):
                return "Error: All fields are required"
            
            # Validate charge for electric vehicles
            if vehicle_type in [VehicleType.ELECTRIC_CAR, VehicleType.ELECTRIC_BIKE]:
                if not 0 <= initial_charge <= 100:
                    return "Error: Charge level must be between 0 and 100"
            
            # Create vehicle using factory
            vehicle = VehicleFactory.create_vehicle(
                vehicle_type, regnum, make, model, color, initial_charge
            )
            
            # Try to park
            result = self._repository.park_vehicle(vehicle)
            
            if result:
                level, slot = result
                slot_type = "EV" if slot.is_ev_slot else "Regular"
                charge_info = ""
                if isinstance(vehicle, ElectricVehicle):
                    charge_info = f" (Charge: {initial_charge}%)"
                return (f"Allocated {slot_type} slot number: {slot.slot_number} "
                       f"on Level {level.level_number}{charge_info}")
            else:
                return "Sorry, parking lot is full"
        
        except Exception as e:
            return f"Error parking vehicle: {str(e)}"
    
    def remove_vehicle(self, slot_number: int) -> str:
        """
        Remove a vehicle from a slot
        FIXED: Only needs slot number - auto-detects level and slot type!
        Returns: Success/failure message
        """
        try:
            if slot_number <= 0:
                return "Error: Invalid slot number"
            
            result = self._repository.remove_vehicle(slot_number)
            
            if result:
                level, slot, vehicle = result
                slot_type = "EV" if slot.is_ev_slot else "Regular"
                return (f"{slot_type} slot number {slot_number} "
                       f"(Level {level.level_number}) is now free")
            else:
                return (f"Unable to remove vehicle from slot {slot_number} "
                       f"(slot may be empty or not exist)")
        
        except Exception as e:
            return f"Error removing vehicle: {str(e)}"
    
    def update_ev_charge(self, slot_number: int, new_charge: int) -> str:
        """
        Update charge level for an electric vehicle
        FIXED: New feature for charge management
        """
        try:
            if not 0 <= new_charge <= 100:
                return "Error: Charge level must be between 0 and 100"
            
            success = self._repository.update_ev_charge(slot_number, new_charge)
            
            if success:
                return f"Updated charge level for slot {slot_number} to {new_charge}%"
            else:
                return f"Error: Slot {slot_number} not found or not an electric vehicle"
        
        except Exception as e:
            return f"Error updating charge: {str(e)}"
    
    def find_slot_by_regnum(self, regnum: str) -> str:
        """Find slot number by registration number"""
        try:
            result = self._repository.find_vehicle_by_regnum(regnum)
            
            if result:
                level, slot, vehicle = result
                slot_type = "EV" if slot.is_ev_slot else "Regular"
                charge_info = ""
                if isinstance(vehicle, ElectricVehicle):
                    charge_info = f", Charge: {vehicle.charge}%"
                return (f"Found: {slot_type} Slot {slot.slot_number}, "
                       f"Level {level.level_number}{charge_info}")
            else:
                return f"Vehicle with registration {regnum} not found"
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def find_slots_by_color(self, color: str) -> str:
        """Find all slot numbers by vehicle color"""
        try:
            results = self._repository.find_vehicles_by_color(color)
            
            if results:
                regular_slots = [f"{slot.slot_number} (L{level.level_number})" 
                               for level, slot, _ in results if not slot.is_ev_slot]
                ev_slots = [f"{slot.slot_number} (L{level.level_number})" 
                           for level, slot, _ in results if slot.is_ev_slot]
                
                output = []
                if regular_slots:
                    output.append(f"Regular slots: {', '.join(regular_slots)}")
                if ev_slots:
                    output.append(f"EV slots: {', '.join(ev_slots)}")
                
                return "\n".join(output)
            else:
                return f"No vehicles with color '{color}' found"
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def find_regnums_by_color(self, color: str) -> str:
        """Find all registration numbers by vehicle color"""
        try:
            results = self._repository.find_vehicles_by_color(color)
            
            if results:
                regular_regnums = [vehicle.regnum 
                                  for level, slot, vehicle in results if not slot.is_ev_slot]
                ev_regnums = [vehicle.regnum 
                             for level, slot, vehicle in results if slot.is_ev_slot]
                
                output = []
                if regular_regnums:
                    output.append(f"Regular vehicles: {', '.join(regular_regnums)}")
                if ev_regnums:
                    output.append(f"Electric vehicles: {', '.join(ev_regnums)}")
                
                return "\n".join(output)
            else:
                return f"No vehicles with color '{color}' found"
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_parking_status(self) -> str:
        """Get status of all parked vehicles"""
        try:
            vehicles = self._repository.get_all_parked_vehicles()
            
            if not vehicles:
                return "No vehicles currently parked"
            
            # Separate regular and EV vehicles
            regular_vehicles = [(level, slot, vehicle) for level, slot, vehicle in vehicles 
                               if not slot.is_ev_slot]
            ev_vehicles = [(level, slot, vehicle) for level, slot, vehicle in vehicles 
                          if slot.is_ev_slot]
            
            output = []
            
            # Regular vehicles
            if regular_vehicles:
                output.append("=== Regular Vehicles ===")
                output.append("Slot\tLevel\tReg No.\t\tColor\t\tMake\t\tModel")
                for level, slot, vehicle in regular_vehicles:
                    output.append(f"{slot.slot_number}\t{level.level_number}\t{vehicle.regnum}\t\t"
                                f"{vehicle.color}\t\t{vehicle.make}\t\t{vehicle.model}")
            
            # Electric vehicles
            if ev_vehicles:
                output.append("\n=== Electric Vehicles ===")
                output.append("Slot\tLevel\tReg No.\t\tColor\t\tMake\t\tModel\tCharge")
                for level, slot, vehicle in ev_vehicles:
                    charge = vehicle.charge if isinstance(vehicle, ElectricVehicle) else 0
                    output.append(f"{slot.slot_number}\t{level.level_number}\t{vehicle.regnum}\t\t"
                                f"{vehicle.color}\t\t{vehicle.make}\t\t{vehicle.model}\t{charge}%")
            
            return "\n".join(output)
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_ev_charge_status(self) -> str:
        """Get charge status of all electric vehicles"""
        try:
            ev_vehicles = self._repository.get_all_ev_vehicles()
            
            if not ev_vehicles:
                return "No electric vehicles currently parked"
            
            output = ["=== Electric Vehicle Charge Levels ==="]
            output.append("Slot\tLevel\tReg No.\t\tCharge %")
            
            for level, slot, vehicle in ev_vehicles:
                output.append(f"{slot.slot_number}\t{level.level_number}\t"
                            f"{vehicle.regnum}\t\t{vehicle.charge}%")
            
            return "\n".join(output)
        
        except Exception as e:
            return f"Error: {str(e)}"
