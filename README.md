# Parking Manager Project

Refactoring and architecture design for a Python parking lot manager. I start from an existing tkinter app, document its anti-patterns, rebuild it with three design patterns (MVP, Repository, Factory), and then scale the thinking up: a Domain-Driven Design analysis and a microservices architecture for a fictional multi-garage operator, **EasyParkPlus**.

Built for the **Software Design and Architecture** course, Quantic School of Business and Technology (MSSE). Solo project.

## Overview

The project has two parts that build on each other.

**Part 1: Refactor the code.** The original Parking Lot Manager is one 40-method `ParkingLot` class that mixes business logic, storage and tkinter calls. I identify 10 anti-patterns, draw UML for the before and after, and rewrite the app so each concern lives in its own layer.

**Part 2: Design the system around it.** For EasyParkPlus, an operator of 10 multi-story garages in Boston, New York and Philadelphia (growing to 14 to 16) with integrated EV charging, I run a DDD analysis with the client, define a shared vocabulary, and derive eight microservices with APIs and a database per service.

## Part 1: Refactoring

### Anti-patterns found in the original app

| # | Anti-pattern | Where |
|---|---|---|
| 1 | God class (40+ methods, many responsibilities) | `ParkingLot` |
| 2 | Business logic tightly coupled to tkinter | `ParkingLot` methods write directly to the text widget |
| 3 | 15+ module-level global variables for UI state | `ParkingManager.py` |
| 4 | Broken inheritance: `ElectricVehicle` does not extend `Vehicle` | `ElectricVehicle.py` |
| 5 | Parent `__init__` called directly instead of `super()` | `Vehicle.py`, `ElectricVehicle.py` |
| 6 | No data access abstraction (raw arrays) | `ParkingLot` |
| 7 | Mixed return types (slot id or `-1`) | `park()` |
| 8 | Inconsistent naming (camelCase, snake_case, abbreviations) | whole codebase |
| 9 | Long, deeply nested methods | `park()`, `status()`, `chargeStatus()` |
| 10 | No error handling or input validation | whole codebase |

Full analysis with impact and evidence: `01_Original_Design/anti_patterns_analysis.md`.

### Design patterns used

| Pattern | Fixes | Implemented in |
|---|---|---|
| **MVP** (Model-View-Presenter) | God class, UI coupling, global state | `models.py`, `presenter.py`, `view.py` |
| **Repository** | No data abstraction | `repository.py` |
| **Factory** | Scattered object creation | `vehicle_factory.py` |

Flow when parking a vehicle: the View collects the form and calls the Presenter, the Presenter validates and asks the Factory to create the vehicle, the Repository finds a slot and stores it, and the Presenter sends the result message back to the View. The View contains no logic, so the Presenter can be tested without a GUI.

Justification for each pattern, and why MVP over MVC: `02_Refactored_Design/design_patterns_justification.md`.

### Other improvements in the refactored code

- Correct inheritance: `Vehicle` is an abstract base class, and `ElectricVehicle`, `ElectricCar` and `ElectricBike` extend it using `super()`
- `VehicleType` enum instead of boolean flags and magic strings
- Encapsulation with `@property`, and a validated charge level (0 to 100)
- `ParkingSlot` and `ParkingLevel` domain classes with global sequential slot numbering across levels, with regular and EV slots numbered separately
- Removing a vehicle needs only the slot number, because the level and slot type are detected automatically
- New features: choose the vehicle type from a dropdown, set an initial charge, and update a charge level later
- Input validation and error messages instead of crashes

### UML

PlantUML diagrams for both versions, in `01_Original_Design/` and `02_Refactored_Design/`:

| Diagram | Original | Refactored |
|---|---|---|
| Class diagram | `UML_Structural_Original.puml` | `UML_Structural_Refactored.puml` |
| Sequence diagram (park a vehicle) | `UML_Behavioral_Original.puml` | `UML_Behavioral_Refactored.puml` |

## Part 2: EasyParkPlus domain design

### Domain-Driven Design analysis

Based on a requirements conversation with the client (Michael), documented in `05_DDD_Analysis/ddd_analysis_report.md`.

| Type | Subdomains |
|---|---|
| Core | Parking space management, EV charging management |
| Supporting | Customer management, billing, facility management |
| Generic | Notifications, integration hub, reporting and analytics |

Five bounded contexts follow from this: Parking Operations, EV Charging, Customer Management, Billing and Facility Management. The analysis includes domain models for each context, integration patterns, and the domain events that connect them (for example `VehicleParked`, `ChargingCompleted`, `PaymentFailed`).

Selected business rules the design has to support: reservations up to 30 days ahead by slot type, entrance-nearest auto-assignment with load balancing, a 15-minute grace period, a 72-hour maximum stay, time-banded pricing with daily, weekly and monthly caps, separate billing for parking and charging, three connector types (Type 2, CCS, CHAdeMO), and 5-year data retention with CCPA compliance.

Supporting documents in `05_DDD_Analysis/`:
- `ubiquitous_language.md` for terms per context and shared across contexts
- `Bounded_Context_Diagram.puml`
- `domain_model_parking.puml` and `domain_model_ev_charging.puml`

### Microservices architecture

Documented in `06_Microservices_Architecture/`. Design principles: one bounded context per service, a database per service, event-driven communication and an API gateway.

| Service | Type | Database |
|---|---|---|
| Parking Operations | Core | `parking_operations_db` |
| EV Charging | Core | `ev_charging_db` |
| Customer Management | Supporting | `customer_management_db` |
| Billing | Supporting | `billing_db` |
| Facility Management | Supporting | `facility_management_db` |
| Notification | Generic | Third-party (for example Twilio, SendGrid) |
| Integration Hub | Generic | None (Google and Apple Maps, payment gateway, CRM, gate hardware) |
| Analytics and Reporting | Generic | `analytics_db` (read-optimized, fed by events) |

The specification (`microservices_complete_specification.md`) also covers the REST endpoints for each service and the database schema per service. The architecture is sized for growth from 10 facilities to 20 or more within five years. Diagram: `architecture_diagram.puml`.

## Tech stack

- **Language:** Python 3.9 or newer
- **GUI:** tkinter (standard library, no extra packages)
- **Modeling:** PlantUML
- **Methods:** MVP, Repository and Factory patterns, Domain-Driven Design, microservices

## Running the application

```bash
# Refactored version
cd 03_Source_Code/refactored
python main.py

# Original version, for comparison
cd 03_Source_Code/original
python ParkingManager.py
```

No dependencies to install. In the app: create a parking lot (regular slots, EV slots, floor), park and remove vehicles, search by registration number or color, view lot status and EV charge levels, and update a charge level.

## Project structure

```
Parking-Manager-Project/
├── 01_Original_Design/
│   ├── anti_patterns_analysis.md
│   ├── UML_Structural_Original.puml
│   └── UML_Behavioral_Original.puml
├── 02_Refactored_Design/
│   ├── design_patterns_justification.md
│   ├── UML_Structural_Refactored.puml
│   └── UML_Behavioral_Refactored.puml
├── 03_Source_Code/
│   ├── original/          # ParkingManager.py, Vehicle.py, ElectricVehicle.py
│   └── refactored/        # main.py, models.py, presenter.py, repository.py,
│                          # vehicle_factory.py, view.py
├── 05_DDD_Analysis/
│   ├── ddd_analysis_report.md
│   ├── ubiquitous_language.md
│   ├── Bounded_Context_Diagram.puml
│   ├── domain_model_parking.puml
│   └── domain_model_ev_charging.puml
└── 06_Microservices_Architecture/
    ├── microservices_complete_specification.md
    └── architecture_diagram.puml
```

## What I learned

Most of the original app's problems come from one decision: letting a single class own everything. Splitting it into View, Presenter, Repository and Factory made each piece small enough to understand and test. Applying DDD to a larger fictional business then showed how the same idea, one clear responsibility per unit, scales from classes to bounded contexts to services.
