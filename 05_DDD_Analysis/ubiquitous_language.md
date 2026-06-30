# Ubiquitous Language - EasyParkPlus System

## Purpose
This document defines the common vocabulary used across all bounded contexts in the EasyParkPlus parking management system. Terms are organized by context to ensure consistent understanding within each domain. Finally, an overview of cross-context shared terms is provided.
---

## Context 1: Parking Operations

###Core Terms

**Facility**: A physical parking location with one or more levels
- Example: "Boston Downtown Facility has 3 levels"

**Level/Floor**: A horizontal section within a facility containing parking slots
- Example: "Level 2 has 150 regular slots"

**Parking Slot**: A designated space where a single vehicle can park
- Example: "Slot R-042 is a regular car space"

**Slot Type**: Classification of parking spaces based on vehicle requirements
- Types: Regular, EV, Handicap (ADA), Compact, Motorcycle, Oversized, Carpool, Family
- Example: "Slot EV-015 is an EV charging slot"

**Slot Status**: Current state of a parking slot
- Values: Available, Occupied, Reserved, Out of Service, Under Maintenance
- Example: "Slot R-100 status changed from Available to Occupied"

**Reservation**: Pre-booking of a parking slot type for a future time period
- Example: "Customer reserved a regular slot for Dec 15, 2-4 PM"

**Parking Session**: The period from when a vehicle enters until it exits the facility
- Example: "Session S-12345 started at 09:00, ended at 17:30"

**Entry Time**: Timestamp when vehicle enters facility (session starts)

**Exit Time**: Timestamp when vehicle leaves facility (session ends)

**Occupancy**: Number of slots currently in use vs. total capacity
- Example: "Facility occupancy: 145/200 (72.5%)"

**Real-time Availability**: Current count of available slots by type

**Auto-assignment**: Automated allocation of optimal slot to entering vehicle
- Rule: Entrance-nearest slot + load balancing across levels

**Grace Period**: 15-minute window after payment before overstay fees apply
- Example: "Payment made at 17:00, grace period until 17:15"

**Max Duration**: Maximum allowed parking time (typically 72 hours)

**Overstay**: Parking beyond the maximum allowed duration

**Lost Ticket**: When customer cannot provide proof of entry
- Resolution: Lookup by registration plate + charge max daily rate

**Peak Hours**: High-demand time periods with premium pricing
- Weekdays: 07:00-10:00, 16:00-19:00

**Time-banded Rate**: Pricing that varies by time of day

**LPR (License Plate Recognition)**: Automated system to identify vehicles at entry/exit

**Gate**: Physical barrier controlling entry/exit from facility or level

**Access Control**: System managing who can enter/park (LPR + QR codes)

---

## Context 2: EV Charging Management

### Core Terms

**Charging Station**: Physical equipment providing electricity to EVs
- Example: "Station CHG-025 has 2 connectors"

**Connector**: Physical interface between station and vehicle
- Types: Type 2 (EU), CCS (Combined Charging System), CHAdeMO (Asian)

**Power Level**: Charging speed classification
- Level 2: 7-19 kW (slow, 4-8 hours full charge)
- DC Fast: 50-150 kW (medium, 30-60 min to 80%)
- Ultra-Fast: 150-350 kW (fast, 15-30 min to 80%)

**Charging Session**: Period from plug-in to disconnect
- Example: "Session CS-789 delivered 45.2 kWh over 42 minutes"

**SOC (State of Charge)**: Battery level percentage (0-100%)
- Example: "Vehicle SOC increased from 25% to 85%"

**Target SOC**: Desired battery level set by customer
- Example: "User set target SOC to 80% for battery health"

**kWh (Kilowatt-hour)**: Unit of energy delivered
- Example: "Session consumed 38.7 kWh"

**kWh Rate**: Cost per kilowatt-hour of electricity
- Level 2: $0.35/kWh, DC Fast: $0.50/kWh, Ultra-Fast: $0.50/kWh

**Charge Completion**: When target SOC is reached or user stops session

**Charging Grace Period**: 15 minutes after completion before idle fees apply

**Idle Fee**: Charge for occupying station after charging completes
- Encourages prompt disconnection for next user

**Authorization Method**: How user starts charging
- Options: Mobile app, RFID card

**Remote Stop**: User-initiated termination of charging via app

**Station Health**: Operational status of charging equipment
- Values: Operational, Degraded, Offline, Under Maintenance

**Connector Status**: Availability state of individual connector
- Values: Available, In Use, Out of Service, Reserved

**Energy Delivered**: Total kWh supplied during session

**Peak Power**: Maximum kW achieved during session

**Session Duration**: Total time from plug-in to disconnect

**Predictive Maintenance**: Forecasting equipment failures before they occur (future feature)

**V2G (Vehicle-to-Grid)**: Technology allowing EVs to return power to grid (future feature)

---

## Context 3: Customer Management

### Core Terms

**Customer**: Individual or entity with account in system
- Types: Individual, Corporate, Fleet, Guest

**Account Type**: Classification of customer
- Individual: Single person
- Corporate: Company with multiple users
- Fleet: Organization with vehicle fleet
- Guest: Pay-by-plate, no account

**Registration/Sign-up**: Process of creating new customer account

**Customer Profile**: Collection of customer information and preferences

**Vehicle Registration**: Adding a vehicle to customer's account
- Required: Registration plate, make, model, color
- Optional: Nickname, is_electric, connector type

**Registration Plate**: Vehicle identifier (license plate number)
- Example: "ABC-1234"

**Membership Tier**: Customer classification affecting rates and benefits
- Tiers: Basic, Premium, Corporate
- Premium: Discounts, priority reservations
- Corporate: Departmental billing, volume discounts

**Corporate Account**: Multi-user business account
- Features: Centralized billing, department tracking, admin controls

**Department**: Sub-unit within corporate account
- Example: "Sales department within Acme Corp account"

**Fleet Account**: Organization managing multiple vehicles
- Features: Vehicle tracking, consolidated billing

**Guest Checkout**: Pay-by-plate for non-account holders
- No pre-registration required

**Payment Method**: Stored billing instrument
- Types: Credit card, Debit card, Apple Pay, Google Pay, PayPal

**Membership Upgrade**: Transition to higher tier (e.g., Basic  Premium)

**Account Status**: State of customer account
- Values: Active, Suspended, Closed

---

## Context 4: Billing & Payment

### Core Terms

**Invoice**: Billing document for parking/charging services
- Contains: Line items, subtotal, taxes, total

**Invoice Line Item**: Individual charge within invoice
- Example: "Parking fee: 8 hours @ $3/hr = $24.00"

**Fee Calculation**: Process of determining charges owed
- Inputs: Duration, slot type, time of day, membership tier

**Parking Fee**: Charges for parking space usage
- Base rates: Regular $3/hr, EV $4/hr, Handicap $1.50/hr, Compact $2/hr

**Charging Fee**: Charges for electricity consumption
- Based on kWh rate × energy delivered

**Rate Cap**: Maximum charge for time period
- Daily: $25, Weekly: $120, Monthly: $300

**Peak Rate**: Higher pricing during high-demand hours
- Applied during peak hours (07:00-10:00, 16:00-19:00 weekdays)

**Overstay Fee**: Penalty for exceeding maximum duration

**Idle Fee**: Penalty for leaving vehicle at charger after completion

**Payment**: Transfer of funds to settle invoice
- Methods: Card, Mobile payment, PayPal

**Payment Status**: State of payment processing
- Values: Pending, Authorized, Captured, Failed, Refunded

**Transaction**: Record of payment attempt/completion

**Failed Payment**: Unsuccessful payment processing
- For members: Invoice system + exit hold
- For guests: Cannot exit until paid

**Refund**: Return of previously paid funds

**Exit Hold**: Preventing vehicle from leaving due to unpaid balance

**Departmental Billing**: Corporate feature splitting charges by department

**Volume Discount**: Reduced rates for high-usage corporate accounts

**Tax**: Government-mandated addition to charges (varies by location)

**Currency**: Monetary unit for transactions (USD in US facilities)

---

## Context 5: Facility Management

### Core Terms

**Facility Configuration**: Settings defining facility capabilities
- Includes: Total capacity, slot type distribution, operating hours, pricing rules

**Capacity Setting**: Allocation of slots by type
- Example: "150 regular, 30 EV, 10 handicap, 10 compact"

**Operating Hours**: Time facility is open for business
- Can vary by day of week

**Pricing Rule**: Configuration defining rates
- Includes: Base rates, peak multipliers, caps

**Maintenance Schedule**: Planned downtime for equipment/facility
- Example: "Level 3 closed for resurfacing Dec 10-15"

**Capacity Adjustment**: Temporary modification of available slots
- Reasons: Maintenance, special events, weather

**Facility Status**: Operational state
- Values: Open, Closed, Limited Capacity, Emergency Closure

**Hardware Configuration**: Settings for physical equipment
- LPR cameras, gates, chargers, payment kiosks

**LPR Camera**: License Plate Recognition camera placement and settings

**Gate Configuration**: Entry/exit barrier settings
- Includes: Access rules, failsafe modes

**Slot Assignment Algorithm**: Rules for auto-assigning slots
- Current: Entrance-nearest + load balancing

**Load Balancing**: Distributing vehicles across levels to optimize flow

**Emergency Protocol**: Procedures for incidents
- Fire, medical emergency, power failure, etc.

**Access Rule**: Configuration controlling who can enter/park
- Example: "Premium members can reserve 48 hours in advance"

**Integration Configuration**: Settings for external system connections
- Google Maps API, Apple Maps API, Payment gateway, CRM

---

## Cross-Context Shared Terms

**Customer/Account**: Referenced in all contexts, but owned by Customer Management

**Vehicle**: Referenced in Parking Operations, EV Charging, Customer Management
- Core attributes consistent across contexts

**Facility**: Owned by Facility Management, referenced by Parking Operations

**Charging Station**: Owned by EV Charging, location managed by Facility Management

**Invoice**: Owned by Billing, triggered by Parking Operations and EV Charging

**Timestamp**: All contexts use ISO 8601 format (e.g., "2025-12-10T15:30:00Z")

**Currency**: All monetary values in USD (until international expansion)

---


