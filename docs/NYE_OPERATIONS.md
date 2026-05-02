# NY&E Railroad — Northern Lights Subdivision Operations Reference

**Status:** Working document — source content for layout website (modelrr.adbyrne.us)
**Scale:** HO (1:87)
**Era:** circa 1905
**Prototype basis:** C&O (Chesapeake & Ohio), freelanced

---

## 1. Railroad Identity

**Road name:** NY&E Railroad _(full name TBD)_
**Subdivision:** Northern Lights Subdivision
**Timetable reference:** No. 4, December 31, 1904 — `Documents/Layout/modelrr/timetable4.pdf`

The NY&E is a freelanced regional carrier modeled on C&O mountain branch line character. The Northern Lights Subdivision runs from the C&O connection at Williamsport northward into mountain resort and mining territory, terminating at Hemlock Crest.

---

## 2. Physical Layout Description

### Two-Level Arrangement

| Level | Content |
|-------|---------|
| Upper | C&O mainline — short modeled section between East staging and West staging |
| Lower | NY&E Northern Lights Subdivision — WP (Williamsport) to HC (Hemlock Crest) |

### C&O Mainline (Upper Level)
A representative section of the C&O mainline. Trains enter from East staging and exit to West staging (or vice versa). No through running — staging-to-staging operation only. The C&O shares the Williamsport station building with the NY&E on the lower level.

### NY&E Branch (Lower Level)
Point-to-point, single main track, south to north. All stations have passing sidings. Southward trains are **superior by direction**. The branch connects to the C&O at Williamsport (WP) and terminates at Hemlock Crest (HC).

### Track Plan
**Software:** XTrackCAD (`https://sourceforge.net/projects/xtrkcad-fork/`)
**Status:** Previous layout file exists (close approximation); new file for current layout needed.
**File location:** _(TBD — create and store in `Trains/docs/` or `Trains/` root)_

---

## 3. Named Locations

"Station" in railroad usage means any named location with operating significance — not only locations with passenger service or CYD equipment. All named locations appear in the timetable.

### Location Type Codes

| Code | Meaning |
|------|---------|
| YL | Yard Limit |
| TO | Train Order station — signal arm present; crews receive and return orders here |
| R | Register station — all trains must report; clearance forms required |
| S | Industry siding — trains stop for switching; no passenger service |
| I | Industry / freight stop — local freight only |

### NY&E Northern Lights Subdivision (MP 0 → 135, south to north)

| ID | Name | MP | Type | CYD | Notes |
|----|------|----|------|-----|-------|
| WP | Williamsport Yard East | 0 | YL, TO, R | — | Freight yard; NY&E coal and general freight staging |
| WP | Williamsport Station | 0 | TO, R | Yes | Passenger station; shared with C&O; local industry switching |
| — | Kiel Co | 4.1 | I | No | Local freight |
| — | O'Haras Lumber and Feed | 5.6 | I | No | Local freight |
| — | O'Haras Coal Service | 15.6 | I | No | Coal service |
| XP | Xina Pass | 37 / 43.5 | TO, R | Yes | Register station; all trains report here; manual block section endpoint |
| — | Quilly Mine #1 | 51.4 | S | No | Coal loading siding |
| BB | Becs Bend | 58.4 | TO | Yes | Train order station |
| JC | Jacks Creek | 76.4 | TO | Yes | Train order station; additional trackage connecting to MC |
| MC | Michelles Cove | 78.2 | TO | Yes | Upgraded from siding; additional trackage to JC |
| — | Quilly Mine #2 | 99.2 | S | No | Coal loading siding |
| SK | Stans Knob | 103.2 | TO | Yes | Mountain resort; hotel directly across main tracks |
| — | Quilly Mine #3 | 112.2 / 118.2 | S | No | Coal loading siding |
| — | Timber Ltd | 128.1 | I | No | Lumber industry |
| HC | Hemlock Crest | 135 | TO, R | Yes | North terminus; register station; upper-class resort area |

### C&O East Central Subdivision — Williamsport Junction

| Name | Notes |
|------|-------|
| Williamsport Yard East | Shared with NY&E; interchange track for car exchange |
| Williamsport Yard West | C&O only |
| East Staging | Cumberland / Erland MD direction |
| West Staging | Covington WV direction |

C&O operations at WP do not use CYD units or digital OS reporting. C&O train schedules appear in the timetable for yard planning purposes only (Yardmaster display, interchange coordination).

---

## 4. Timetable Reference

**Timetable No. 4, December 31, 1904** is the primary operating authority. Source PDF: `NYELayoutDocs/alt/timetable.pdf`. The digital representation is `timetable.json` loaded by RR_Server at startup.

The Northern Lights Subdivision runs **12 northward and 12 southward trains daily** (all marked Daily):

| Class | Northward | Southward | Service types |
|-------|-----------|-----------|---------------|
| First | 1, 3, 11 | 2, 4, 52 | Passenger, Freight |
| Second | 21, 23, 25 | 22, 24, 26 | Passenger |
| Third | 101, 111, 121, 131, 141 | 102, 112, 122, 132, 142 | Coal, Coke, Freight |

Key northward departures from Williamsport Station (passenger trains): No. 1 at 07:10 AM, No. 3 at 03:45 PM, No. 21 at 01:31 PM, No. 23 at 11:00 AM, No. 25 at 08:15 AM. Freight and coal trains depart from Williamsport Yard East.

The timetable also covers the **C&O East Central Subdivision** through Williamsport (Erland/Cumberland MD ↔ Covington WV). See Section 3 for location list. See Section 11 for timetable management.

---

## 5. Motive Power

_To be documented. Circa 1905 C&O prototype steam._

| Road # | Class / Type | Assignment | Notes |
|--------|-------------|------------|-------|
| TBD | | | |

---

## 6. Car Inventory

_To be documented._

### Freight
| Car Type | Road | Qty | Service |
|----------|------|-----|---------|
| TBD | | | |

### Passenger
| Car Type | Road | Qty | Service |
|----------|------|-----|---------|
| TBD | | | |

### Work Equipment
| Type | Notes |
|------|-------|
| TBD | |

---

## 7. Operating Rules

_Derived from Timetable No. 4 and NY&E operating history._

### General
- Timetable and Train Order (TT&TO) operations
- Southward trains are superior by direction
- Extra trains operate under Train Order authority only (no timetable authority); identified by engine number: "Extra 101 North"
- Maximum speed: 1 real second per shortest car in consist
- **Runaway coal cars have absolute priority over all trains — all trains clear immediately**

### Register Stations and Clearances
- All trains must register at Xina Pass (XP)
- Clearance forms required at all register stations (WP, XP, HC)
- Clearance forms also required at any station where a train originates
- Dispatcher controls the Williamsport–Xina Pass manual block section via clearance form times

### Train Orders and Sections
- Dispatcher issues Train Orders via the dispatcher web app; station agent copies to paper and delivers to crew
- TO signal arm raises when order is issued; lowers when ACKed and released by Dispatcher
- Trains may run in sections established by Train Order; section number must be included in all OS reports for that train

### Road Crew Rules
- Flagmen must be posted at all switchbacks north of Xina Pass
- Trains must stop and protect whenever halted on the main line away from a station
- Freight trains must move caboose to the other end of the train when changing direction at a station
- OS report submitted at each station on arrival and departure (train number, section, direction)

### C&O Interchange at Williamsport
- WP yard is shared with C&O East Central trains
- Yardmaster must keep the main clear for C&O through trains
- Interchange track must be available when C&O trains arrive to drop or pick up cars
- Car exchange tracked via the Car Card & Waybill system (see Section 10)

---

## 8. Reference Documents

| Document | Location | Notes |
|----------|----------|-------|
| Timetable No. 4 (Dec 31, 1904) | `Documents/Layout/modelrr/timetable4.pdf` | Primary operating authority |
| Railway Construction (1905) | `Downloads/Books/Trains/` | Period reference |
| Passenger Terminals (1905) | `Downloads/Books/Trains/` | Period reference |
| 1905 Equipment Register | `Downloads/Books/Trains/` | Motive power / car reference |
| Station Fig. 172 (NH combo) | `Trains/SmallStation.png` | Station design prototype |
| Layout Control System | `Trains/IOTtrains/docs/SYSTEM_ARCHITECTURE.md` | IoT control architecture |
| MQTT Specification | `Trains/IOTtrains/docs/MQTT_SPEC.md` | IoT messaging reference |
| XTrackCAD layout file | TBD | Track plan — new file needed |
| Previous layout archive | `Trains/NYELayoutDocs/` | XTrackCAD files, old ops documents, timetable source data |
| Implementation Plan | `Trains/IOTtrains/docs/IMPLEMENTATION_PLAN.md` | Session-by-session build plan |

---

## 9. Operating Roles

These duty cards define responsibilities during an operating session. In small sessions one person may perform multiple roles. **The Dispatcher and Yardmaster are always separate individuals.**

### Dispatcher

**Works at the RPi5 dispatcher terminal (separate room or location from the yard).**

**Session setup:**
- Verify all station CYD units are online before starting the clock
- Confirm session day and starting railroad time from saved state
- Start the fast clock

**During operations:**
- Monitor the OS log — all train movements at all stations (train #, section, direction, RR time)
- Monitor consist reports and train-ready signals from Yardmaster
- Maintain session lineup — track actual vs. scheduled departure times
- Cancel scheduled trains via Train Order to affected stations
- Authorize Extra trains via Train Order naming engine number ("Extra 101 North")
- Issue Train Orders — freeform 1905-style text, addressed to one or more stations
- Issue Clearance Forms — at WP, XP, HC, and any station where a train originates
- Control TO signal arms — raise N or S arm when order issued; lower when released
- Notify Yardmaster of trains inbound from Xina Pass (expected arrival time)
- Notify Yardmaster of lineup changes:
  - Departure time changes: 1 railroad hour advance notice minimum
  - New or extra trains: 2 railroad hours advance notice minimum
- Monitor C&O schedule for awareness of interchange and main-line conflicts

**The Dispatcher does not communicate directly with road crews.** All crew communication is through Train Orders delivered at stations.

---

### Yardmaster

**Works at the Williamsport yard (RPi3 + 7" touchscreen terminal).**

**Ongoing:**
- Monitor NLS departure lineup (timetable + Dispatcher adjustments)
- Monitor arrival notifications from Dispatcher
- Monitor C&O timetable (read-only) — keep main clear for through trains; keep interchange track available for C&O car drops and pickups
- Keep yard track assignments organized
- Capture empty cars available in yard for loading assignment

**Per outbound train (30 railroad minutes before departure):**
- Call road crew
- Direct Hostler to have engine prepared
- Assemble consist from Car Cards and Waybills; note any special handling requirements (e.g., reefer cars requiring icing before departure)
- Submit consist report digitally: engine #, caboose #, loaded car count, empty car count
- Mark train as Ready (combined with consist submission) — formal signal to Dispatcher

**Per inbound train:**
- Align yard entrance switches on Dispatcher notification
- Direct crew to assigned track on arrival
- Switch station passenger tracks 10 railroad minutes after passenger train arrives
- Direct Hostler to service arriving engine; arrange icing for inbound reefer cars as needed

**C&O interchange:**
- Stage outbound interchange cars on interchange track before C&O arrival
- Receive inbound interchange cars from C&O; assign to appropriate NY&E trains via waybills

---

### Hostler

**Works under Yardmaster direction. Treated as yard crew, not road crew.**

- Service arriving engines: coal, water, sand, oil, inspection
- Move engines to and from service tracks as directed
- Prepare departing engine; report ready to Yardmaster verbally
- Perform local industry switching and car spotting as directed (freight house, ice house, team track, warehouses)
- Ice reefer cars at ice house as directed by Yardmaster

_No IoT unit required — all communication with Yardmaster is verbal._

---

### Station Agent

**One CYD per station. In small sessions this role is typically performed by the road crew at their current station.**

- Submit OS report when train arrives at or departs from station: train number, section number, direction
- Receive Train Orders on CYD display; copy to paper; ACK when crew copies are made
- Receive Clearance Forms on CYD display; issue to crew; ACK when crew has it
- Monitor fast clock and next train status line

_Station agent does not issue orders or communicate directly with the Dispatcher except through OS and ACK functions._

---

## 10. Car Cards & Waybills

The CC&W system is the freight car routing backbone. Every car on the layout or in staging has a physical Car Card and an active Waybill.

### Car Card
- Permanent physical card (envelope-like pocket) that travels with the car
- Contains: car ID (road name + number), car type
- Printed once; replaced only if damaged

### Waybill
- Inserted into the Car Card pocket
- Contains: origin, destination industry, commodity
- Replaced each session cycle as the owner assigns new routing

### Special Waybills
Some car types require additional handling steps beyond simple routing:
- **Refrigerator cars (reefers):** must be iced at the ice house before loading and again after unloading. Yardmaster directs Hostler to spot reefers at the ice house; cannot depart until iced.
- **Empty car capture:** empty cars available in the yard may be assigned to outbound trains by the Yardmaster when a waybill calls for an empty at a specific industry.

### How it works operationally
- The Yardmaster reads Car Cards and Waybills to assemble each train's consist and to identify any special handling requirements
- The Waybill tells the crew which industry to spot each car at
- Trains pick up and set out cars at industries according to their Waybills
- Cars routed to/from C&O are marked for interchange; Yardmaster stages them on the interchange track

### Consist reporting
- The Yardmaster submits a digital consist summary (engine #, caboose #, loaded count, empty count) derived from reading the Car Cards
- Car-level routing detail remains on the paper Waybills

---

## 11. Management Functions

Management functions are performed by the layout owner between operating sessions. These are not part of the operational IoT system but produce outputs the system depends on.

### Timetable Management
- Create and version timetables; each version has a version number and release date
- Generate printed timetable in Timetable No. 4 format (all operators receive a personal copy)
- Generate String Table (train scheduling diagram showing meets and crossing points)
- Generate per-station condensed schedule cards (previous station / current station / next station times)
- Export `timetable.json` for RR_Server to load
- Source methodology: `NYELayoutDocs/alt/Stringline.ods` — track segment profile, class speeds, stop delays

### CC&W Management
- Maintain car database (car ID, type, road name, special requirements)
- Maintain industry database (name, station, commodities accepted/shipped, track capacity, special handling such as icing)
- Assign waybill routing between sessions (which car goes where each cycle)
- Print car cards (one-time per car) and waybills (each session cycle)
- _Future: owner-triggered session events — e.g., a reefer spotted at an industry triggers an icing requirement during the session_

### Print Materials
All materials below are printed by the owner before each session as needed:
- Full timetable (all operators receive a personal copy)
- Per-station condensed schedule cards
- Duty cards (Dispatcher, Yardmaster, Hostler, Station Agent)
- Waybills (session cycle)
- Train Register forms (blank, per station — formal paper record of all train movements)
- Train order pads (blank forms for crew copies of Train Orders)
