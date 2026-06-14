# Next Session Plan — NY&E Timetable & String Table

_Updated 2026-06-08_

---

## Status at end of this session

| Item | State |
|------|-------|
| `timetable.json` — NLS trains (both directions) | ✅ Complete |
| `timetable.json` — COE subdivision (10 C&O trains) | ✅ Complete |
| `yard.json` — Williamsport Yard track data | ✅ Complete (lengths approximate; XTrkCAD survey needed) |
| `docs/NYE_StringTable.svg` + `generate_stringtable.py` | ✅ Complete — workable V1 |
| QM3 eliminated from timetable + docs | ✅ Done |
| Timber Ltd moved to JC siding | ✅ Done (mp TBD) |
| All docs + README updated and pushed | ✅ Done |

---

## Priority 1 — String Table review and refinement

Review the current `docs/NYE_StringTable.svg` against the historical `NYELayoutDocs/alt/DispatcherSheet.ods` string table and note any discrepancies:

- Are all NLS trains present and on the correct direction?
- Do dwell widths (bold vs thin) look right at each station?
- C&O marks at WP — are they readable at this scale?
- Station label rotation and spacing — any collisions?
- Is the 40px/hr vertical scale comfortable for reading meets?

Likely refinements:
- Add actual Setout/Pickup notes to NLS freight train schedule entries in timetable.json (needed to trigger bold dwell and spur stubs)
- Add "Wait for No. X" meet notes to trigger red meet dots
- Confirm spur milepost for Timber Ltd within JC from XTrkCAD

---

## Priority 2 — XTrkCAD data survey

**2026-06-14 (export bug fixes + milepost unit finalised):** `nye_layout_data.json` re-exported. Milepost unit finalised — timetable.json now stores **export MP values directly** (e.g. XP=45.1, HC=208.1); 1 MP = 12 layout inches. Do NOT ×12. JC confirmed 16-car passing siding (was export layer bug). QM1 Coke/Lead track lengths resolved. yard.json updated to v1.2 (track_ids corrected, Yard Lead added). NYE_StringTable.svg regenerated. track_schematic.svg, XTRKCAD_DATA_REQUIREMENTS.md updated. NYE_ETT_NLS.html + NYE_ETT_COE.html generated. Timetable display policy: sidings shown as cars only, not track length in feet.

**2026-06-13 (updated export):** `nye_layout_data.json` re-exported with structural schema changes. See `docs/XTRKCAD_DATA_REQUIREMENTS.md`.

**Schema changes in 2026-06-13 export:**
- Stations: now have `milepost_entry` + `milepost_exit` pre-computed (no longer derive exit from entry + siding length)
- Industries: `spur_length_ft`/`spur_length_cars` removed; now have `car_spots` + `branch_milepost`
- `yard_tracks` added as new top-level array (WP, QM1, QM2 tracks with XTrkCAD-measured lengths)

**Resolved by 2026-06-13 export:**

| Location | Resolved |
|----------|---------|
| XP | milepost, milepost_exit, siding_length_cars (3) ✓ |
| BB | milepost, milepost_exit (5638.6), siding_length_cars (4) ✓ |
| SK | milepost (14508.7), milepost_exit (14834.9), siding_length_cars (3) ✓ |
| HC | milepost, milepost_exit, siding_length_cars (3) ✓ |
| MC | milepost (8914.9), milepost_exit (9570.3 via @MC_EXIT), siding_length_cars (11) ✓ |
| JC | milepost ✓; confirmed NOT a switchback; no passing siding (milepost_exit + siding_length_cars → null) |
| TIMBER | milepost (9457.7 on JC reversing lead), car_spots (3) ✓ |
| KIEL, OHARAS_LF | milepost + car_spots ✓ |
| OHARAS_CS | milepost corrected (578.0, co-located with LF), car_spots (1) ✓ |
| QM1 | milepost corrected (5112.3), car_spots (2) ✓ |
| QM2 | milepost corrected (9629.9), car_spots (2) ✓ |
| WP yard tracks | XTrkCAD-measured lengths in yard.json v1.1 ✓ |

**Still open:**

| Location | Missing data |
|----------|-------------|
| MC | Topology confirm — `milepost_exit` value (9570.3) trusted from @MC_EXIT reference point but two-switch geometry not yet surveyed |
| JC | Service track length (for Yardmaster, not timetable) |
| KIEL | `milepost_exit` — industrial switchback exit not measured |
| WP RUN track | `length_ft` not in export |
| QM1 Coke + Lead | `length_ft = 0` in export (note placement bug — do not use) |

---

## Priority 3 — ETT generator (`generate_ett.py`)

Write `docs/scripts/generate_ett.py` to produce:

1. **NLS Employee Timetable** (`docs/NYE_ETT_NLS.html`) — traditional two-sided:
   - Northward trains: left columns
   - Southward trains: right columns
   - Stations: centre column (with type codes YL/TO/R)
   - 12-hour times with AM/PM headers
   - Meet notes below time cells
   - Flagging-required stations marked

2. **C&O Reference Table** (`docs/NYE_ETT_COE.html`) — compact table for YM binder:
   - Trains 91/92/93/94 (coal) + 5/6/7/12/23/32 (passenger)
   - WP arrive/depart times only
   - Direction column
   - Print-friendly: fits on half-sheet

### Industry display rules (decided 2026-06-13)

All industries must appear in the ETT with name + car spots. Two display modes:

**Station industries** (`within_limits_of` is set):
- Indented sub-entry within the parent station's centre column
- Show: name, `car_spots`; no time cells

**On-line industries** (`within_limits_of: null`, own milepost):
- Own condensed row at their milepost, positioned between the correct station pair
- Show: name, `car_spots`; no time cells; visually distinct from station rows (e.g. smaller font, no rule lines)
- Examples: KIEL (mp 456), OHARAS_LF (mp 578), OHARAS_CS (mp 932)

**timetable.json field reference for ETT:**
- Stations: read `siding_length_cars` (passing-track capacity)
- Industries: read `car_spots` (operational spotting capacity)
- `within_limits_of: null` + own milepost = on-line industry row
- `within_limits_of: "<ID>"` = sub-entry under that station

### Industry yards (QM1, QM2) — separate data, not yet available

QM1 and QM2 each have multiple named tracks (empties, loads, loading tracks).
These are not in `yard.json` (which covers WP classification yard only).
A future `industry_yards.json` will hold this data once XTrkCAD zero-length
track issues are resolved. ETT generator does not need this for initial version.

---

## Priority 4 — Session 2.3 (Clearance Forms)

Dispatcher app clearance form feature. Prerequisites:
- `timetable.json` data complete (done ✅)
- YM design confirmed (done ✅ — `docs/YARDMASTER_DESIGN.md`)

See `IOTtrains/docs/IMPLEMENTATION_PLAN.md` for session spec.

---

## Priority 5 — Session 2.0a/2.0b (Yardmaster Terminal)

Backend (2.0a) then UI + RPi3 provisioning (2.0b).

Hardware: RPi3-1 or RPi3-3 + ELECROW 7" (pk=106).

See `IOTtrains/docs/YARDMASTER_DESIGN.md` for full spec.

---

## Open questions / decisions deferred

- **Interactive string table** (web component): FastAPI route `/stringtable`, scrolling viewport, current-time-at-top, 2-hour configurable window, extra-train planning aid. Design doc (`DISPATCHER_STRINGTABLE_DESIGN.md`) to be written after YM 2.0 is implemented.
- **Timber Ltd milepost**: confirmed 9457.7 on JC reversing lead from XTrkCAD export (2026-06-13). ✓
- **MC milepost reconciliation**: resolved — old values were estimates; MC now at 9132.9 from XTrkCAD. ✓
- **MC milepost_exit**: two-switch geometry; exit MP requires topology analysis in XTrkCAD.
- **NLS freight train work notes**: `timetable.json` schedules don't yet have Setout/Pickup notes — needed for string table to show bold dwells and spur stubs at industries.
