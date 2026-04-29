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

## 3. Station Reference

Stations listed south → north. All have passing sidings.

| ID | Name | MP | Role | Notes |
|----|------|----|------|-------|
| WP | Williamsport | 0 | South terminus, junction, yard | Shared with C&O mainline; physical yard; local industries |
| XP | Xina Pass | 37 / 43.5 | Register station | All trains register; train orders + clearance forms |
| BB | Becs Bend | 58.4 | Train order station | |
| JC | Jacks Creek | 76.4 | Train order station | Additional trackage connecting to MC |
| MC | Michelles Cove | 78.2 | Train order station | Was siding-only; upgraded to station; additional trackage to JC |
| SK | Stans Knob | 103.2 | Train order station | Mountain resort; hotel directly across main tracks |
| HC | Hemlock Crest | 135 | Register station, north terminus | Upper-class resort area; return-trip clearances issued here |

### Special Operating Notes (from Timetable No. 4)
- **Runaway coal cars have priority over all trains**
- Flagmen required at all switchbacks north of Xina Pass
- All trains must register at Xina Pass (XP)
- Southward trains superior by direction

---

## 4. Industrial Sidings

From Timetable No. 4 (northward mile posts from WP):

| Industry | MP | Notes |
|----------|----|-------|
| Williamsport yard industries | 0 | _(specifics TBD)_ |
| Kiel Co | 4.1 | |
| O'Haras Lumber and Feed | 5.6 | |
| O'Haras Coal Service | 15.6 | |
| Quilly Mine #1 | 51.4 | Near Xina Pass |
| Quilly Mine #2 | 99.2 | Near Stans Knob |
| Quilly Mine #3 | 112.2 / 118.2 | Between SK and HC |
| Timber Ltd | 128.1 | Near Hemlock Crest |

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

## 7. Operating Rules Summary

_Derived from Timetable No. 4. Formal rulebook TBD._

- Timetable and Train Order operation
- Dispatcher issues Train Orders via telegraph; agent copies and delivers to crew
- Clearance forms required at register stations (WP, XP) and north terminus (HC)
- Extra trains operate under train orders only (no timetable authority)
- Coal runaway cars have absolute priority — all trains clear immediately
- RFID tags on locomotives and cabooses for OS reporting assistance (Phase 4)

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
