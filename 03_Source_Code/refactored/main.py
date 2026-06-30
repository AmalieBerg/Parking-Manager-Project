"""
Main Entry Point for Parking Lot Manager
Initializes MVP pattern and starts the application
"""

from presenter import ParkingPresenter
from view import ParkingLotView


def main():
    """
    Initialize and run the Parking Lot Manager application
    
    MVP Pattern initialization:
    1. Create Presenter (contains business logic)
    2. Create View (GUI), passing Presenter reference
    3. Start GUI event loop
    """
    # Create Presenter (Model is created within Presenter)
    presenter = ParkingPresenter()
    
    # Create View with Presenter reference
    view = ParkingLotView(presenter)
    
    # Start GUI
    view.run()


if __name__ == '__main__':
    main()
