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

Items still null in timetable.json and yard.json that need physical measurement or XTrkCAD query:

| Location | Missing data |
|----------|-------------|
| BB, JC, MC, SK | `milepost_exit` (switchback exit switch MP) |
| BB, JC, MC, SK | `siding_length_cars` |
| TIMBER | `milepost` (exact MP within JC siding) |
| WP RUN track | `length_model_in` |
| All yard tracks | Verify lengths from XTrkCAD (currently approximate) |
| MC | Confirm milepost: ops doc says 78.2; timetable.json says 99.2 — **reconcile** |

Reference: `docs/XTRKCAD_DATA_REQUIREMENTS.md`

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
- **Timber Ltd milepost**: confirm exact position in JC siding once XTrkCAD survey done.
- **MC milepost reconciliation**: ops doc shows 78.2, timetable.json has 99.2 — verify against XTrkCAD.
- **NLS freight train work notes**: `timetable.json` schedules don't yet have Setout/Pickup notes — needed for string table to show bold dwells and spur stubs at industries.
