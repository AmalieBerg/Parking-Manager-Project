"""
View Layer - implements MVP Pattern
GUI using tkinter - decoupled from business logic
FIXED: Dropdown for vehicle type, charge input, no "Remove EV?" checkbox
"""

import tkinter as tk
from tkinter import ttk
from presenter import ParkingPresenter
from models import VehicleType


class ParkingLotView:
    """
    View in MVP pattern
    - Handles all GUI elements
    - NO business logic
    - Communicates only with Presenter
    FIXED: Better UX with dropdown, charge management
    """
    
    def __init__(self, presenter: ParkingPresenter):
        self._presenter = presenter
        
        # Create main window
        self.root = tk.Tk()
        self.root.geometry("700x900")
        self.root.resizable(0, 0)
        self.root.title("Parking Lot Manager - Refactored")
        
        # Initialize GUI variables
        self._init_variables()
        
        # Build GUI
        self._build_gui()
    
    def _init_variables(self):
        """
        Initialize all tkinter variables
        FIXED: Removed unused level_remove_value
        FIXED: Added vehicle_type_var and charge_var
        """
        self.num_value = tk.StringVar()
        self.ev_value = tk.StringVar()
        self.make_value = tk.StringVar()
        self.model_value = tk.StringVar()
        self.color_value = tk.StringVar()
        self.reg_value = tk.StringVar()
        self.level_value = tk.StringVar()
        self.vehicle_type_var = tk.StringVar(value="Car")  # NEW: Dropdown selection
        self.charge_var = tk.StringVar(value="50")  # NEW: Charge level 0-100
        self.slot1_value = tk.StringVar()
        self.slot2_value = tk.StringVar()
        self.reg1_value = tk.StringVar()
        self.slot_value = tk.StringVar()
        self.update_charge_slot_var = tk.StringVar()  # NEW: For updating charge
        self.update_charge_value_var = tk.StringVar(value="80")  # NEW
    
    def _build_gui(self):
        """Build all GUI elements"""
        row = 0
        
        # Header
        label_head = tk.Label(self.root, text='Parking Lot Manager (Refactored)', 
                             font='Arial 14 bold')
        label_head.grid(row=row, column=0, padx=10, columnspan=4)
        row += 1
        
        # Lot Creation Section
        row = self._build_lot_creation_section(row)
        
        # Car Management Section
        row = self._build_car_management_section(row)
        
        # Search Section
        row = self._build_search_section(row)
        
        # Output text field
        self.tfield = tk.Text(self.root, width=80, height=18)
        self.tfield.grid(column=0, row=row, padx=10, pady=10, columnspan=4)
    
    def _build_lot_creation_section(self, row: int) -> int:
        """Build lot creation section"""
        label_head = tk.Label(self.root, text='Lot Creation', font='Arial 12 bold')
        label_head.grid(row=row, column=0, padx=10, columnspan=4)
        row += 1
        
        # Regular spaces
        lbl_num = tk.Label(self.root, text='Number of Regular Spaces', font='Arial 12')
        lbl_num.grid(row=row, column=0, padx=5)
        
        num_entry = tk.Entry(self.root, textvariable=self.num_value, width=6, font='Arial 12')
        num_entry.grid(row=row, column=1, padx=4, pady=2)
        
        # EV spaces
        lbl_ev = tk.Label(self.root, text='Number of EV Spaces', font='Arial 12')
        lbl_ev.grid(row=row, column=2, padx=5)
        
        ev_entry = tk.Entry(self.root, textvariable=self.ev_value, width=6, font='Arial 12')
        ev_entry.grid(row=row, column=3, padx=4, pady=4)
        row += 1
        
        # Level
        lbl_level = tk.Label(self.root, text='Floor Level', font='Arial 12')
        lbl_level.grid(row=row, column=0, padx=5)
        
        level_entry = tk.Entry(self.root, textvariable=self.level_value, width=6, font='Arial 12')
        level_entry.grid(row=row, column=1, padx=4, pady=4)
        level_entry.insert(tk.INSERT, "1")
        row += 1
        
        # Create button
        create_btn = tk.Button(self.root, command=self._on_create_lot, 
                              text="Create Parking Lot", font="Arial 12",
                              bg='lightblue', fg='black', activebackground="teal",
                              padx=5, pady=5)
        create_btn.grid(row=row, column=0, padx=4, pady=4)
        row += 1
        
        return row
    
    def _build_car_management_section(self, row: int) -> int:
        """
        Build car management section
        FIXED: Dropdown for vehicle type instead of checkboxes
        FIXED: Charge level input for electric vehicles
        """
        label_car = tk.Label(self.root, text='Car Management', font='Arial 12 bold')
        label_car.grid(row=row, column=0, padx=10, columnspan=4)
        row += 1
        
        # Make and Model
        lbl_make = tk.Label(self.root, text='Make', font='Arial 12')
        lbl_make.grid(row=row, column=0, padx=5)
        
        make_entry = tk.Entry(self.root, textvariable=self.make_value, width=12, font='Arial 12')
        make_entry.grid(row=row, column=1, padx=4, pady=4)
        
        lbl_model = tk.Label(self.root, text='Model', font='Arial 12')
        lbl_model.grid(row=row, column=2, padx=5)
        
        model_entry = tk.Entry(self.root, textvariable=self.model_value, width=12, font='Arial 12')
        model_entry.grid(row=row, column=3, padx=4, pady=4)
        row += 1
        
        # Color and Registration
        lbl_color = tk.Label(self.root, text='Color', font='Arial 12')
        lbl_color.grid(row=row, column=0, padx=5)
        
        color_entry = tk.Entry(self.root, textvariable=self.color_value, width=12, font='Arial 12')
        color_entry.grid(row=row, column=1, padx=4, pady=4)
        
        lbl_reg = tk.Label(self.root, text='Registration #', font='Arial 12')
        lbl_reg.grid(row=row, column=2, padx=5)
        
        reg_entry = tk.Entry(self.root, textvariable=self.reg_value, width=12, font='Arial 12')
        reg_entry.grid(row=row, column=3, padx=4, pady=4)
        row += 1
        
        # FIXED: Dropdown for vehicle type (replaces checkboxes)
        lbl_vehicle_type = tk.Label(self.root, text='Vehicle Type', font='Arial 12')
        lbl_vehicle_type.grid(row=row, column=0, padx=5)
        
        vehicle_type_dropdown = ttk.Combobox(
            self.root, 
            textvariable=self.vehicle_type_var,
            values=["Car", "Motorcycle", "Electric Car", "Electric Bike"],
            state="readonly",
            width=15,
            font='Arial 11'
        )
        vehicle_type_dropdown.grid(row=row, column=1, padx=4, pady=4)
        vehicle_type_dropdown.bind("<<ComboboxSelected>>", self._on_vehicle_type_changed)
        
        # FIXED: Charge level input (shows for electric vehicles)
        self.lbl_charge = tk.Label(self.root, text='Initial Charge %', font='Arial 12')
        self.lbl_charge.grid(row=row, column=2, padx=5)
        self.lbl_charge.grid_remove()  # Hidden by default
        
        self.charge_entry = tk.Entry(self.root, textvariable=self.charge_var, 
                                     width=6, font='Arial 12')
        self.charge_entry.grid(row=row, column=3, padx=4, pady=4)
        self.charge_entry.grid_remove()  # Hidden by default
        row += 1
        
        # Park button
        park_btn = tk.Button(self.root, command=self._on_park_car, text="Park Vehicle",
                           font="Arial 11", bg='lightblue', fg='black',
                           activebackground="teal", padx=5, pady=5)
        park_btn.grid(column=0, row=row, padx=4, pady=4)
        row += 1
        
        # Remove vehicle section - FIXED: No "Remove EV?" checkbox!
        lbl_remove = tk.Label(self.root, text='Remove Vehicle', font='Arial 12 bold')
        lbl_remove.grid(row=row, column=0, padx=10, columnspan=2)
        row += 1
        
        lbl_slot = tk.Label(self.root, text='Slot #', font='Arial 12')
        lbl_slot.grid(row=row, column=0, padx=5)
        
        slot_entry = tk.Entry(self.root, textvariable=self.slot_value, width=12, font='Arial 12')
        slot_entry.grid(row=row, column=1, padx=4, pady=4)
        
        remove_btn = tk.Button(self.root, command=self._on_remove_car, text="Remove Vehicle",
                             font="Arial 11", bg='lightcoral', fg='black',
                             activebackground="red", padx=5, pady=5)
        remove_btn.grid(column=2, row=row, padx=4, pady=4)
        row += 1
        
        # FIXED: New section for updating EV charge
        lbl_update_charge = tk.Label(self.root, text='Update EV Charge', font='Arial 12 bold')
        lbl_update_charge.grid(row=row, column=0, padx=10, columnspan=2)
        row += 1
        
        lbl_charge_slot = tk.Label(self.root, text='EV Slot #', font='Arial 12')
        lbl_charge_slot.grid(row=row, column=0, padx=5)
        
        charge_slot_entry = tk.Entry(self.root, textvariable=self.update_charge_slot_var, 
                                     width=6, font='Arial 12')
        charge_slot_entry.grid(row=row, column=1, padx=4, pady=4)
        
        lbl_new_charge = tk.Label(self.root, text='New Charge %', font='Arial 12')
        lbl_new_charge.grid(row=row, column=2, padx=5)
        
        new_charge_entry = tk.Entry(self.root, textvariable=self.update_charge_value_var, 
                                    width=6, font='Arial 12')
        new_charge_entry.grid(row=row, column=3, padx=4, pady=4)
        row += 1
        
        update_charge_btn = tk.Button(self.root, command=self._on_update_charge, 
                                      text="Update Charge",
                                      font="Arial 11", bg='lightyellow', fg='black',
                                      activebackground="gold", padx=5, pady=5)
        update_charge_btn.grid(column=0, row=row, padx=4, pady=4)
        row += 1
        
        # Spacer
        spacer = tk.Label(self.root, text="")
        spacer.grid(row=row, column=0)
        row += 1
        
        return row
    
    def _build_search_section(self, row: int) -> int:
        """Build search and status section"""
        # Find by registration
        slot_reg_btn = tk.Button(self.root, command=self._on_slot_by_reg,
                                text="Get Slot ID by Registration #",
                                font="Arial 11", bg='lightblue', fg='black',
                                activebackground="teal", padx=5, pady=5)
        slot_reg_btn.grid(column=0, row=row, padx=4, pady=4)
        
        slot1_entry = tk.Entry(self.root, textvariable=self.slot1_value, width=12, font='Arial 12')
        slot1_entry.grid(row=row, column=1, padx=4, pady=4)
        
        # Find by color
        slot_color_btn = tk.Button(self.root, command=self._on_slot_by_color,
                                  text="Get Slot ID by Color",
                                  font="Arial 11", bg='lightblue', fg='black',
                                  activebackground="teal", padx=5, pady=5)
        slot_color_btn.grid(column=2, row=row, padx=4, pady=4)
        
        slot2_entry = tk.Entry(self.root, textvariable=self.slot2_value, width=12, font='Arial 12')
        slot2_entry.grid(row=row, column=3, padx=4, pady=4)
        row += 1
        
        # Registration by color
        reg_color_btn = tk.Button(self.root, command=self._on_reg_by_color,
                                 text="Get Registration # by Color",
                                 font="Arial 11", bg='lightblue', fg='black',
                                 activebackground="teal", padx=5, pady=5)
        reg_color_btn.grid(column=0, row=row, padx=4, pady=4)
        
        reg1_entry = tk.Entry(self.root, textvariable=self.reg1_value, width=12, font='Arial 12')
        reg1_entry.grid(row=row, column=1, padx=4, pady=4)
        
        # EV charge status
        charge_btn = tk.Button(self.root, command=self._on_charge_status,
                             text="EV Charge Status",
                             font="Arial 11", bg='lightblue', fg='black',
                             activebackground="teal", padx=5, pady=5)
        charge_btn.grid(column=2, row=row, padx=4, pady=4)
        row += 1
        
        # Overall status
        status_btn = tk.Button(self.root, command=self._on_status,
                             text="Current Lot Status",
                             font="Arial 11", bg='PaleGreen1', fg='black',
                             activebackground="PaleGreen3", padx=5, pady=5)
        status_btn.grid(column=0, row=row, padx=4, pady=4)
        row += 1
        
        return row
    
    # Event handlers - communicate with Presenter
    
    def _on_vehicle_type_changed(self, event):
        """
        Show/hide charge input based on vehicle type selection
        FIXED: Dynamic UI based on selection
        """
        vehicle_type = self.vehicle_type_var.get()
        if "Electric" in vehicle_type:
            self.lbl_charge.grid()
            self.charge_entry.grid()
        else:
            self.lbl_charge.grid_remove()
            self.charge_entry.grid_remove()
    
    def _on_create_lot(self):
        """Handle create lot button click"""
        try:
            regular_capacity = int(self.num_value.get())
            ev_capacity = int(self.ev_value.get())
            level_number = int(self.level_value.get())
            
            result = self._presenter.create_parking_lot(regular_capacity, ev_capacity, level_number)
            self._display_message(result)
        except ValueError:
            self._display_message("Error: Please enter valid numbers")
    
    def _on_park_car(self):
        """
        Handle park vehicle button click
        FIXED: Uses VehicleType enum from dropdown
        FIXED: Includes charge level for electric vehicles
        """
        try:
            # Map dropdown text to VehicleType enum
            type_map = {
                "Car": VehicleType.CAR,
                "Motorcycle": VehicleType.MOTORCYCLE,
                "Electric Car": VehicleType.ELECTRIC_CAR,
                "Electric Bike": VehicleType.ELECTRIC_BIKE
            }
            
            vehicle_type_str = self.vehicle_type_var.get()
            vehicle_type = type_map.get(vehicle_type_str, VehicleType.CAR)
            
            # Get charge level if electric vehicle
            initial_charge = 0
            if "Electric" in vehicle_type_str:
                try:
                    initial_charge = int(self.charge_var.get())
                except ValueError:
                    self._display_message("Error: Charge level must be a number")
                    return
            
            result = self._presenter.park_vehicle(
                self.reg_value.get(),
                self.make_value.get(),
                self.model_value.get(),
                self.color_value.get(),
                vehicle_type,
                initial_charge
            )
            self._display_message(result)
        except Exception as e:
            self._display_message(f"Error: {str(e)}")
    
    def _on_remove_car(self):
        """
        Handle remove vehicle button click
        FIXED: Only needs slot number - no level, no "is EV" checkbox!
        """
        try:
            slot_number = int(self.slot_value.get())
            result = self._presenter.remove_vehicle(slot_number)
            self._display_message(result)
        except ValueError:
            self._display_message("Error: Please enter a valid slot number")
    
    def _on_update_charge(self):
        """
        Handle update charge button click
        FIXED: New feature for updating EV charge levels
        """
        try:
            slot_number = int(self.update_charge_slot_var.get())
            new_charge = int(self.update_charge_value_var.get())
            
            result = self._presenter.update_ev_charge(slot_number, new_charge)
            self._display_message(result)
        except ValueError:
            self._display_message("Error: Please enter valid numbers")
    
    def _on_slot_by_reg(self):
        """Handle find slot by registration"""
        result = self._presenter.find_slot_by_regnum(self.slot1_value.get())
        self._display_message(result)
    
    def _on_slot_by_color(self):
        """Handle find slots by color"""
        result = self._presenter.find_slots_by_color(self.slot2_value.get())
        self._display_message(result)
    
    def _on_reg_by_color(self):
        """Handle find registrations by color"""
        result = self._presenter.find_regnums_by_color(self.reg1_value.get())
        self._display_message(result)
    
    def _on_status(self):
        """Handle status button click"""
        result = self._presenter.get_parking_status()
        self._display_message(result)
    
    def _on_charge_status(self):
        """Handle EV charge status button click"""
        result = self._presenter.get_ev_charge_status()
        self._display_message(result)
    
    def _display_message(self, message: str):
        """Display a message in the output text field"""
        self.tfield.insert(tk.INSERT, message + "\n\n")
    
    def run(self):
        """Start the GUI event loop"""
        self.root.mainloop()
