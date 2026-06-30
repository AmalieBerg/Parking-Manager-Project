"""
Vehicle Factory - implements Factory Pattern
Centralizes vehicle creation logic
FIXED: Uses VehicleType enum instead of boolean flags
"""

from models import (
    Vehicle, Car, Motorcycle, ElectricCar, ElectricBike, VehicleType
)


class VehicleFactory:
    """
    Factory for creating vehicles
    - Encapsulates creation logic
    - Returns appropriate vehicle type
    FIXED: Uses VehicleType enum for cleaner interface
    """
    
    @staticmethod
    def create_vehicle(vehicle_type: VehicleType, regnum: str, make: str, 
                      model: str, color: str, initial_charge: int = 0) -> Vehicle:
        """
        Create a vehicle of the specified type
        FIXED: Single enum parameter instead of two booleans
        
        Args:
            vehicle_type: VehicleType enum value
            regnum: Registration number
            make: Vehicle make/manufacturer
            model: Vehicle model
            color: Vehicle color
            initial_charge: Initial charge level for EVs (0-100)
        
        Returns:
            Vehicle instance of appropriate type
        
        Raises:
            ValueError: If vehicle_type is invalid
        """
        if vehicle_type == VehicleType.CAR:
            return Car(regnum, make, model, color)
        
        elif vehicle_type == VehicleType.MOTORCYCLE:
            return Motorcycle(regnum, make, model, color)
        
        elif vehicle_type == VehicleType.ELECTRIC_CAR:
            return ElectricCar(regnum, make, model, color, initial_charge)
        
        elif vehicle_type == VehicleType.ELECTRIC_BIKE:
            return ElectricBike(regnum, make, model, color, initial_charge)
        
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
    
    @staticmethod
    def get_available_types() -> list[VehicleType]:
        """Get list of all available vehicle types"""
        return [
            VehicleType.CAR,
            VehicleType.MOTORCYCLE,
            VehicleType.ELECTRIC_CAR,
            VehicleType.ELECTRIC_BIKE
        ]
