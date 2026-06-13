# XTrkCAD Data Requirements for NY&E Layout Control System

**Version:** 1.1
**Date:** 2026-06-13
**Layout file:** `~/XTrkCAD/nyelayout/new_york_and_eastern.xtc`
**JSON export:** `~/XTrkCAD/nyelayout/reports/nye_layout_data.json` (generated 2026-06-13)

---

## 1. Purpose

The layout control system's operational data lives in `IOTtrains/RR_Server/data/timetable.json`.
Many fields are currently `null` pending physical layout measurement:

- `milepost_exit` — exit MP for every online station (XP entry is known; all others TBD)
- `milepost_exit` — exit MPs for switchback stations (BB, JC, MC, SK) where the main rejoins after reversal
- `siding_length_cars` — passing siding capacity for all online stations (XP, BB, JC, MC, SK)
- Industry spur branch mileposts and lengths

These will be populated from an XTrkCAD-generated data export once the MCP tool is complete.
The export must be **repeatable** — re-run after each layout remodel session that moves or extends track.

---

## 2. Data Required

### 2.1 Online Stations (XP, BB, JC, MC, SK)

| Field | Description | Unit |
|-------|-------------|------|
| `station_id` | Matches `timetable.json` location `id` | — |
| `milepost_entry` | MP at south (entry) end of passing siding | prototype miles |
| `milepost_exit` | MP at north (exit) end of passing siding | prototype miles |
| `siding_length_ft` | Physical length of passing siding track | real feet |
| `siding_length_cars` | Car capacity (computed: `floor(siding_length_ft * 2)`) | cars |
| `switchback` | Whether siding is a reversing switchback | boolean |

**MP convention:** 1 MP = 1 real foot. MPs increase northward (WP=0, HC=135).

**Siding length:** measure from the south clearance point to the north clearance point (end of the runaround, exclusive of the main-track turnouts).

**Switchback `milepost_exit`:** for switchback stations, the exit MP is where the outbound train re-enters the main track after reversing — this may differ significantly from the entry MP. The gap between entry and exit represents the length of the reversing lead.

**Minimum siding standard:** all online stations have a minimum 3 ft passing siding (6 HO cars). Actual lengths from XTrkCAD survey.

### 2.2 Industries and Sidings

| Field | Description | Unit |
|-------|-------------|------|
| `industry_id` | Matches `timetable.json` location `id` | — |
| `connected_station` | Station whose siding the spur branches from (`within_limits_of`) | — |
| `branch_milepost` | MP at spur branch point on the main or siding | prototype miles |
| `spur_length_ft` | Physical length of spur track | real feet |
| `spur_length_cars` | Car capacity (computed: `floor(spur_length_ft * 2)`) | cars |
| `switchback` | Whether the spur is itself a reversing switchback | boolean |

**Industry ↔ station mapping (from timetable.json):**

| Industry | `within_limits_of` | Notes |
|----------|--------------------|-------|
| KIEL | — (near WP) | Industrial switchback off main |
| OHARAS_LF | — (near WP) | Simple spur |
| OHARAS_CS | — (near WP) | Simple spur |
| QM1 | XP | Mine spur; crews exchange cars at XP siding |
| QM2 | MC | Mine spur; accessible from MC siding |
| TIMBER | JC | Lumber industry; moved to JC siding (mp TBD within JC limits) |

### 2.3 Mainline Segments (between consecutive stations)

| Field | Description | Unit |
|-------|-------------|------|
| `from_station` | Station id at south end | — |
| `to_station` | Station id at north end | — |
| `length_ft` | Mainline length from entry MP of `from` to entry MP of `to` | real feet |

Segments: WP→XP, XP→BB, BB→JC, JC→MC, MC→SK, SK→HC.

---

## 3. Output Format

The MCP tool produces `layout_data.json` (location TBD — suggest `IOTtrains/RR_Server/data/`):

```json
{
  "generated": "2026-06-08T00:00:00Z",
  "layout": "Northern Lights Overview",
  "scale": "HO",
  "stations": [
    {
      "station_id": "XP",
      "milepost_entry": 37.0,
      "milepost_exit": 43.5,
      "siding_length_ft": null,
      "siding_length_cars": null,
      "switchback": false
    }
  ],
  "industries": [
    {
      "industry_id": "QM1",
      "connected_station": "XP",
      "branch_milepost": 51.4,
      "spur_length_ft": null,
      "spur_length_cars": null,
      "switchback": true
    }
  ],
  "segments": [
    {
      "from_station": "WP",
      "to_station": "XP",
      "length_ft": null
    }
  ]
}
```

A merge script reads `layout_data.json` and updates the corresponding `null` fields in `timetable.json`
in-place, leaving all non-null fields untouched.

---

## 4. XTrkCAD Annotation Conventions

For the MCP tool to match XTrkCAD track segments to timetable locations, the following must be
established in `layout.xtc` before running the export:

### 4.1 Track labels

Every passing siding and industry spur must carry the matching `timetable.json` `id` as its XTrkCAD
track label:

| XTrkCAD label | Segment |
|---------------|---------|
| `XP` | Xina Pass passing siding |
| `BB` | Becs Bend passing siding |
| `JC` | Jacks Creek passing siding |
| `MC` | Michelles Cove passing siding |
| `SK` | Stans Knob passing siding |
| `KIEL` | Kiel Co switchback spur |
| `OHARAS_LF` | O'Haras Lumber & Feed spur |
| `OHARAS_CS` | O'Haras Coal Service spur |
| `QM1` | Quilly Mine #1 spur |
| `QM2` | Quilly Mine #2 spur |
| `TIMBER` | Timber Ltd spur (within JC limits) |

### 4.2 MP reference calibration

XTrkCAD MP values must be calibrated so that:
- MP 0.0 = Williamsport Yard east end (WP)
- MPs increase northward toward HC
- Scale: 1 MP = 1 real foot (HO scale, prototype distance)

### 4.3 Layer mapping

| XTrkCAD layer | Content | Role in export |
|---------------|---------|----------------|
| 0 (Main) | Mainline track | MP measurements, segment lengths |
| 4 (Homasote) | Sidings, spurs, yard tracks | Siding and spur lengths |
| 1 (Hidden) | Staging / C&O upper level | Excluded from export |

---

## 5. XTrkCAD MCP Tool API

The tool must expose these operations (proposed names — adjust to MCP bridge conventions):

| Tool | Arguments | Returns |
|------|-----------|---------|
| `get_station_siding` | `station_id` | entry MP, exit MP, siding length ft, switchback |
| `get_industry_spur` | `industry_id` | branch MP, spur length ft, switchback |
| `get_segment_length` | `from_station`, `to_station` | mainline length ft |
| `export_layout_data` | — | full `layout_data.json` |
| `list_labeled_segments` | — | all labeled track segments (for validation) |

---

## 6. Track Schematic Integration

Once `layout_data.json` is produced, update the track schematic
(`docs/diagrams/track_schematic.svg`) to annotate actual siding lengths on each station:

- Add length label (e.g., `4.2 ft / 8 cars`) inside or below each passing siding
- Update station tooltips or notes for the dispatcher display version

The schematic is intended for three uses (design decisions deferred):
1. **Print** — static PDF for the ops session packet
2. **Dispatcher display** — live or rendered SVG on the RPi5 dispatcher screen
3. **JMRI panel** — import as a panel background or use JMRI's built-in schematic editor

---

## 7. Field Status (updated 2026-06-13 from nye_layout_data.json)

**MP note:** timetable.json `milepost` values are now XTrkCAD track-footage (1 MP = 1 track foot from WP=0). They are NOT prototype miles. Only XP, BB, and SK have station house sidings (passing track for meets); other stations have service/industry track only.

| Location ID | `milepost` | `milepost_exit` | `siding_length_cars` | Notes |
|-------------|-----------|-----------------|----------------------|-------|
| WP | 0 ✓ | — | — | Origin |
| KIEL | 455.6 ✓ | null | 2 ✓ | Industrial switchback; exit TBD |
| OHARAS_LF | 578.0 ✓ | — | 2 ✓ | Simple spur |
| OHARAS_CS | 932.1 ✓ | — | 2 ✓ | Simple spur |
| XP | 3931.7 ✓ | 4097.6 ✓ | 3 ✓ | Station house siding; 165.9 ft |
| QM1 | 4866.6 ✓ | — | 2 ✓ | Spur within XP limits; switchback |
| BB | 5370.7 ✓ | 5580.4 ✓ | 4 ✓ | Station house siding; 209.7 ft; exit = entry + siding |
| JC | 7475.4 ✓ | — | null | NOT a switchback (confirmed XTrkCAD); service track only; siding_length null |
| TIMBER | 9457.7 ✓ | — | 2 ✓ | Within JC limits; on JC reversing lead |
| MC | 9132.9 ✓ | **null** | null | Switchback, two-switch geometry; exit at main-to-passing switch (TBD from topology) |
| QM2 | 9121.5 ✓ | — | 2 ✓ | Spur within MC limits; branches just before MC entry |
| SK | 14988.4 ✓ | 15135.7 ✓ | 3 ✓ | Station house siding; 147.3 ft; exit = entry + siding |
| HC | 18121.4 ✓ | 18285.3 ✓ | 3 ✓ | Terminal service track; 163.9 ft |

**Remaining open items:**
- MC `milepost_exit` — requires topology analysis to locate the main-to-passing-track switch MP
- JC `siding_length_cars` — service track length not yet in export
- KIEL `milepost_exit` — industrial switchback exit not measured
