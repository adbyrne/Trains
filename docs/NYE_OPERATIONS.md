# NY&E Railroad — Northern Lights Subdivision Operations Reference

**Status:** Working document — source content for layout website (modelrr.adbyrne.us)
**Scale:** HO (1:87)
**Era:** circa 1905
**Prototype basis:** C&O (Chesapeake & Ohio), freelanced

---

## 1. Railroad Identity

**Road name:** New York and Eastern Railroad (NY&E)
**Subdivision:** Northern Lights Subdivision
**Timetable reference:** No. 4, December 31, 1904 — machine-readable: `Trains/IOTtrains/RR_Server/data/timetable.json`

The NY&E is a freelanced regional carrier modeled on C&O mountain branch line character. The Northern Lights Subdivision runs from the C&O connection at Williamsport northward into mountain resort and mining territory, terminating at Hemlock Crest.

---

## 2. Physical Layout Description

### Two-Level Track Arrangement at Williamsport

_Note: "Upper" and "lower" refer to track elevation/line at Williamsport — not to physical benchwork construction levels._

| Track | Content |
|-------|---------|
| Upper | C&O mainline — short modeled section between East staging and West staging |
| Lower | NY&E Northern Lights Subdivision — WP (Williamsport) to HC (Hemlock Crest) |

### C&O Mainline (Upper Track)
A representative section of the C&O mainline. Trains enter from East staging and exit to West staging (or vice versa). No through running — staging-to-staging operation only. The C&O shares the Williamsport station building with the NY&E on the lower track.

### NY&E Branch (Lower Track)
Point-to-point, single main track, south to north. All stations have passing sidings. Southward trains are **superior by direction**. The branch connects to the C&O at Williamsport (WP) and terminates at Hemlock Crest (HC).

### Track Plan
**Software:** XTrackCAD (`https://sourceforge.net/projects/xtrkcad-fork/`)
**Status:** Layout remodel in progress — current file is ~90% the same as previous layout; new industries and station ideas may be incorporated as remodel proceeds.
**File location:** `~/XTrkCAD/nyelayout/layout.xtc` — room 18'×25.4', 78 turnouts, 312.6 ft mainline. Reports in same directory.
**Previous layout archive:** `Trains/NYELayoutDocs/` — XTrackCAD files, old timetable, string tables, dispatcher docs, waybills.

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
| — | Timber Ltd | within JC limits (mp TBD) | I | No | Lumber industry; siding within limits of Jacks Creek |
| HC | Hemlock Crest | 135 | TO, R | Yes | North terminus; register station; upper-class resort area |

### C&O East Central Subdivision — Williamsport Junction

| Name | Notes |
|------|-------|
| Williamsport Yard East | Shared with NY&E; interchange track for car exchange; used by C&O freight trains |
| Williamsport Yard West | C&O only |
| Williamsport | Station building east of the yard; shared with NY&E; used by C&O passenger trains |
| East Staging | Cumberland / Erland MD direction |
| West Staging | Covington WV direction |

C&O freight trains use the yard (Williamsport Yard East/West). C&O passenger trains use the Williamsport station building. C&O operations at WP do not use CYD units or digital OS reporting. C&O train schedules appear in the timetable for yard planning purposes only (Yardmaster display, interchange coordination).

---

## 4. Timetable Reference

**Timetable No. 4, December 31, 1904** is the primary operating authority. Source file: `Trains/NYELayoutDocs/alt/timetable.ods`. The digital representation is `timetable.json` loaded by RR_Server at startup.

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

Ten steam locomotives on the active roster. All NY&E road engines are Bachmann HO. C&O #1592 and Pennsylvania #1492 are foreign road units that operate exclusively on C&O tracks at Williamsport; NY&E engines operate exclusively on the NY&E branch and do not run on C&O tracks.

| Road # | Type | Road Name | Max Cars | DCC Addr | Manufacturer | Sound |
|--------|------|-----------|----------|----------|--------------|-------|
| 10 | 0-6-0 | NY&E | 6 | 10 | Bachmann | No |
| 11 | 0-6-0 | NY&E | 6 | 11 | Bachmann | No |
| 12 | 0-6-0 | NY&E | 6 | 12 | Bachmann | No |
| 14 | 0-6-0 | NY&E | 6 | 14 | Bachmann | No |
| 21 | 4-4-0 | NY&E | 6 | 21 | Bachmann | Yes |
| 22 | 4-4-0 | NY&E | 6 | 22 | Bachmann | Yes |
| 30 | 2-6-0 | NY&E | 6 | 30 | IHC | No |
| 46 | 4-6-0 | NY&E | 6 | 46 | Bachmann | No |
| 1492 | 4-4-0 | Pennsylvania | 6 | 20 | IHC | No |
| 1592 | 2-6-6-2 | C&O | 12 | 66 | Bachmann | Yes |

---

## 6. Car Inventory

94 freight cars on the active roster. Each car is individually tracked for maintenance. Car type codes follow AAR classification.

### Boxcars (XM) — 14 cars

| Code | Road Name | Road # | Color | Length |
|------|-----------|--------|-------|--------|
| XM | QA&P Rwy | 115 | Brown | 36' |
| XM | StL S_W | 16794 | Brown | 36' |
| XM | Penn. Lines | 559941 | Brown | 36' |
| XM | Penn. Lines | 559946 | Brown | 36' |
| XM | NKP | 10755 | Brown | 36' |
| XM | NKP | 10580 | Brown | 36' |
| XM | D&H Co | 19258 | Brown | 36' |
| XM | M,SP&SSM | 14825 | Brown | 36' |
| XM | CM | 5347 | Brown | 36' |
| XM | D&RG | 63494 | Brown | 36' |
| XM | IP&C RW | 2 | Brown | 36' |
| XM | SP | 12778 | Brown | 36' |
| XM | CCC&STL | 4744 | Brown | 36' |
| XM | CCC&STL | 4748 | Brown | 36' |

### Reefers (RS) — 14 cars

| Code | Road Name | Road # | Color | Length |
|------|-----------|--------|-------|--------|
| RS | Sudbury | 105 | Brown | 36' |
| RS | HERX | 731 | Brown | 36' |
| RS | DSDX | 149 | Green | 36' |
| RS | DSDX | 1490 | Green | 36' |
| RS | Illinois Central | 55401 | Yellow | 36' |
| RS | Boston & Maine | 12749 | Yellow | 36' |
| RS | URTCo | 91021 | Yellow | 36' |
| RS | URTCo | 40680 | Yellow | 36' |
| RS | URTCo | 40676 | Yellow | 36' |
| RS | NADX | 2652 | White | 36' |
| RS | AMSX | 12028 | White | 36' |
| RS | CKKX | 2661 | Red | 36' |
| RS | GPEX | 908 | Brown | 36' |
| RS | LBPX | 102 | Blue | 36' |

### Stock Cars (SM) — 3 cars

| Code | Road Name | Road # | Color | Length |
|------|-----------|--------|-------|--------|
| SM | CC&O | 2723 | Brown | 36' |
| SM | CC&O | 2748 | Brown | 36' |
| SM | GN | 7530 | Brown | 36' |

### Flat Cars (FM) — 39 cars

All NY&E road, black, 32'.

| Code | Road # | Code | Road # | Code | Road # |
|------|--------|------|--------|------|--------|
| FM | 900 | FM | 920 | FM | 940 |
| FM | 901 | FM | 923 | FM | 941 |
| FM | 902 | FM | 924 | FM | 942 |
| FM | 903 | FM | 925 | FM | 943 |
| FM | 904 | FM | 927 | FM | 944 |
| FM | 905 | FM | 928 | FM | 945 |
| FM | 908 | FM | 930 | FM | 947 |
| FM | 914 | FM | 931 | FM | 948 |
| FM | 915 | FM | 932 | FM | 950 |
| — | — | FM | 933 | FM | 951 |
| — | — | FM | 934 | FM | 952 |
| — | — | FM | 935 | FM | 953 |
| — | — | FM | 937 | FM | 954 |
| — | — | FM | 938 | FM | 955 |
| — | — | — | — | FM | 957 |
| — | — | — | — | FM | 958 |

### Hoppers (HM) — 24 cars

All NY&E road, black, 22'.

| Code | Road # | Code | Road # | Code | Road # |
|------|--------|------|--------|------|--------|
| HM | 110 | HM | 120 | HM | 135 |
| HM | 113 | HM | 123 | HM | 136 |
| HM | 114 | HM | 124 | HM | 137 |
| HM | 115 | HM | 125 | HM | 138 |
| HM | 116 | HM | 126 | HM | 140 |
| HM | 117 | HM | 127 | HM | 145 |
| HM | 118 | HM | 128 | HM | 147 |
| HM | 119 | HM | 130 | — | — |

### Passenger Cars

No passenger cars currently on the roster.

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

### Switchback OS Rule

Switchback stations are BB (Becs Bend), MC (Michelles Cove), and SK (Stans Knob). WP and HC (termini), XP (Xina Pass), and JC (Jacks Creek, a 16-car passing siding) are not switchback stations; nor are industries (Quilly Mines QM1/QM2, Kiel Co, O'Haras, Timber Ltd). At switchback stations the train reverses and swaps engine/caboose positions before continuing. The OS rule depends on whether the train has work at that location:

- **No work:** Train is **not OS until engine and caboose are reconnected** after the reversal. Station agent submits the OS report at that point.
- **Work to be done:** Train OSs **on arrival** (before reversal). Train must **take the siding immediately on arrival**. OS is not re-submitted after reconnection.

The station agent CYD will display a reminder at switchback stations to prompt the correct procedure.

### C&O Interchange at Williamsport
- WP yard services all C&O freight — both East Central and westbound (Covington WV direction)
- Yardmaster must keep the main clear for C&O through trains
- Interchange track must be available when C&O trains arrive to drop or pick up cars
- Car exchange tracked via the Car Card & Waybill system (see Section 10)

---

## 8. Reference Documents

| Document | Location | Notes |
|----------|----------|-------|
| Timetable No. 4 (Dec 31, 1904) | `Trains/NYELayoutDocs/alt/timetable.ods` | Legacy source (ODS); superseded by timetable.json |
| Timetable No. 4 — machine data | `Trains/IOTtrains/RR_Server/data/timetable.json` | Single source of truth; NLS + COE subdivisions |
| Timetable No. 4 — string table | `Trains/docs/NYE_StringTable.svg` | Time-distance diagram; generated by `docs/scripts/generate_stringtable.py` |
| Williamsport Yard data | `Trains/IOTtrains/RR_Server/data/yard.json` | Track IDs, lengths, capacities |
| Railway Construction (1905) | `Downloads/Books/Trains/` | Period reference |
| Passenger Terminals (1905) | `Downloads/Books/Trains/` | Period reference |
| 1905 Equipment Register | `Downloads/Books/Trains/` | Motive power / car reference |
| Station Fig. 172 (NH combo) | `Trains/SmallStation.png` | Station design prototype |
| Layout Control System | `Trains/IOTtrains/docs/SYSTEM_ARCHITECTURE.md` | IoT control architecture |
| MQTT Specification | `Trains/IOTtrains/docs/MQTT_SPEC.md` | IoT messaging reference |
| XTrackCAD layout file | `~/XTrkCAD/nyelayout/layout.xtc` | Track plan — in progress, ~90% of final layout |
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

### Equipment Maintenance

Maintenance is a management function performed by the layout owner between operating sessions. Intervals are counted in operating sessions, not calendar time.

**Inspection Schedules**

Locomotives and freight cars follow separate inspection schedules. Specific intervals are TBD and will be set once operating cadence is established.

| Equipment Class | Inspection Interval | Minimum Checks |
|----------------|---------------------|----------------|
| Steam locomotives | TBD sessions | Wheels/axles, motor brushes, drive gear lubrication, lamp function, DCC decoder address/function verify |
| Freight cars | TBD sessions | Wheels/axles (rotation, gauge, no flat spots), couplers (operation, spring tension), trucks (free swing) |

**Bad Order Process**

Equipment is placed **Bad Order** when a defect is found during an operating session or inspection. Bad order equipment is pulled from service immediately and not assigned to consists until released by the owner.

1. **Defect reported** — road crew reports defect verbally to Yardmaster at the next station stop
2. **Equipment pulled** — Yardmaster removes the car or locomotive from the consist; holds it at WP on arrival
3. **Bad order tag applied** — owner attaches a physical bad order tag to the equipment
4. **Repair scheduled** — owner logs the defect and schedules a repair session; equipment remains out of service
5. **Release** — after repair, owner inspects and removes the bad order tag; equipment returned to the active roster

_Future yardmaster feature: digital bad order reporting and tracking via the Yardmaster page — flag a car or locomotive as bad order, record the defect description, and block bad order equipment from consist assignment until the owner releases it._
