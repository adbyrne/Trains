# XTrkCAD Data Requirements for NY&E Layout Control System

**Version:** 1.3
**Date:** 2026-06-14 (updated export — milepost unit corrected)
**Layout file:** `~/XTrkCAD/nyelayout/new_york_and_eastern.xtc`
**JSON export:** `~/XTrkCAD/nyelayout/reports/nye_layout_data.json` (generated 2026-06-14)

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
| `milepost_entry` | MP at south (entry) end of passing siding | layout inches (MP × 12) |
| `milepost_exit` | MP at north (exit) end of passing siding | layout inches (MP × 12) |
| `siding_length_ft` | Physical length of passing siding track | real feet |
| `siding_length_cars` | Car capacity (computed: `floor(siding_length_ft * 2)`) | cars |
| `switchback` | Whether siding is a reversing switchback | boolean |

**MP convention:** 1 MP = 12 layout inches (layout-distance based; ignores prototype scale). MPs increase northward (WP=0, HC≈2497).

**Siding length:** measure from the south clearance point to the north clearance point (end of the runaround, exclusive of the main-track turnouts).

**Switchback `milepost_exit`:** for switchback stations, the exit MP is where the outbound train re-enters the main track after reversing — this may differ significantly from the entry MP. The gap between entry and exit represents the length of the reversing lead.

**Minimum siding standard:** all online stations have a minimum 3 ft passing siding (6 HO cars). Actual lengths from XTrkCAD survey.

### 2.2 Industries and Sidings

| Field | Description | Unit |
|-------|-------------|------|
| `industry_id` | Matches `timetable.json` location `id` | — |
| `connected_station` | Station whose siding the spur branches from (`within_limits_of`); null for on-line industries | — |
| `branch_milepost` | MP at spur branch point on the main or siding | layout inches (MP × 12) |
| `car_spots` | Operational spotting capacity (from stations.yaml, not derived from spur length) | cars |
| `switchback` | Whether the spur is itself a reversing switchback | boolean |

Note: `spur_length_ft` and `spur_length_cars` are no longer in the export. Use `car_spots` instead.

**Industry ↔ station mapping (from timetable.json):**

| Industry | `within_limits_of` | Notes |
|----------|--------------------|-------|
| KIEL | — (near WP) | Industrial switchback off main |
| OHARAS_LF | — (near WP) | Simple spur |
| OHARAS_CS | — (near WP) | Simple spur |
| QM1 | XP | Mine spur; crews exchange cars at XP siding |
| QM2 | MC | Mine spur; accessible from MC siding |
| TIMBER | JC | Lumber industry; on JC reversing lead (mp 1303, physically within MC station limits) |

### 2.3 Mainline Segments (between consecutive stations)

| Field | Description | Unit |
|-------|-------------|------|
| `from_station` | Station id at south end | — |
| `to_station` | Station id at north end | — |
| `length_ft` | Mainline length from entry MP of `from` to entry MP of `to` | real feet |

Segments: WP→XP, XP→BB, BB→JC, JC→MC, MC→SK, SK→HC.

---

## 3. Output Format

The MCP tool produces `nye_layout_data.json` at `~/XTrkCAD/nyelayout/reports/`:

```json
{
  "generated": "2026-06-14T17:12:45Z",
  "layout": "new_york_and_eastern",
  "scale": "HO",
  "stations": [
    {
      "station_id": "XP",
      "milepost_entry": 45.14,
      "milepost_exit": 53.096,
      "siding_length_ft": 693.008,
      "siding_length_cars": 15,
      "main_length_ft": 686.385,
      "main_length_cars": 15,
      "switchback": false
    }
  ],
  "industries": [
    {
      "industry_id": "QM1",
      "connected_station": "XP",
      "branch_milepost": 55.874,
      "car_spots": 2,
      "switchback": true
    }
  ],
  "segments": [
    {
      "from_station": "WP",
      "to_station": "XP",
      "length_ft": 3931.659
    }
  ],
  "yard_tracks": [
    {
      "yard_id": "WP",
      "label": "Arrival/Departure",
      "track_id": 367,
      "length_ft": 512.262,
      "car_capacity": 11
    }
  ]
}
```

**Note on units:** `milepost_entry`/`milepost_exit`/`branch_milepost` in the export are in layout MP (1 MP = 12 layout inches). Convert to timetable layout-inch values by multiplying by 12. Segment `length_ft` values are in prototype feet (layout inches × 87 / 12).

**Known issues resolved in 2026-06-14 export:**
- WP `milepost_exit` terminus artefact — now correctly null in timetable
- JC siding detection — JC has a confirmed 16-car passing siding (was export layer bug; now correct)
- QM1 Coke + Lead `length_ft = 0` — note placement bug resolved; real lengths now in export

Data is consumed by manually syncing into `timetable.json` (mileposts, siding_length_cars) and `yard.json` (yard track lengths). No automated merge script exists yet.

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
- Scale: 1 MP = 12 layout inches (layout-distance based; ignores prototype scale)

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

## 7. Field Status (updated 2026-06-14 from nye_layout_data.json)

**MP note:** timetable.json `milepost` values are in **layout inches** (export MP × 12; 1 MP = 12 layout inches from WP=0). They are NOT prototype miles or feet.

| Location ID | `milepost` | `milepost_exit` | `siding_length_cars` | Notes |
|-------------|-----------|-----------------|----------------------|-------|
| WP | 0 ✓ | — | — | Origin / terminus |
| KIEL | 62.8 ✓ | null | 2 ✓ | Industrial switchback; exit not measured |
| OHARAS_LF | 79.6 ✓ | — | 2 ✓ | Simple spur |
| OHARAS_CS | 79.6 ✓ | — | 1 ✓ | Co-located with LF; coal delivery 1 spot |
| XP | 541.7 ✓ | 637.2 ✓ | 15 ✓ | Long station limits; 693 ft siding |
| QM1 | 670.5 ✓ | — | 2 ✓ | Spur within XP limits; switchback |
| BB | 739.9 ✓ | 776.8 ✓ | 6 ✓ | Switchback; 274 ft siding |
| JC | 1029.9 ✓ | 1129.6 ✓ | 16 ✓ | NOT a switchback; passing siding 723 ft |
| TIMBER | 1303.0 ✓ | — | 3 ✓ | Within JC limits; on JC reversing lead (physically within MC station limits) |
| MC | 1228.2 ✓ | 1318.5 ✓ | 11 ✓ | Switchback; 480 ft siding; exit trusted from @MC_EXIT ref point |
| QM2 | 1256.7 ✓ | — | 2 ✓ | Spur within MC limits |
| SK | 1998.9 ✓ | 2043.8 ✓ | 7 ✓ | Switchback; 308 ft siding |
| HC | 2496.6 ✓ | — | 7 ✓ | North terminus; service siding 340 ft |

**Remaining open items:**
- MC `milepost_exit` topology confirm — value 1318.5 trusted from @MC_EXIT reference point; two-switch geometry not yet surveyed
- KIEL `milepost_exit` — industrial switchback exit not measured
- JC service track length — for Yardmaster display only; not needed for timetable
