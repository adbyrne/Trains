#!/usr/bin/env python3
"""
generate_ett.py — NY&E Employee Timetable generator

Produces:
  docs/NYE_ETT_NLS.html  — NLS Employee Timetable (traditional two-sided format)
  docs/NYE_ETT_COE.html  — C&O East Central Reference Table (compact half-sheet)

Format:
  NB trains (left columns) | Stations (centre) | SB trains (right columns)
  Stations listed WP (top) → HC (bottom).
  Northward trains read top-to-bottom; southward trains read bottom-to-top.
  12-hour times: a=AM, p=PM (e.g. 7:10a, 3:45p).
  On-line industries: condensed row at their milepost position.
  Station industries: indented sub-row under parent station.
"""

import json
import html as _html
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
DATA = ROOT / "IOTtrains" / "RR_Server" / "data" / "timetable.json"
OUT_NLS = HERE.parent / "NYE_ETT_NLS.html"
OUT_COE = HERE.parent / "NYE_ETT_COE.html"


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def fmt12(t):
    """Convert '07:10' → '7:10a', '15:45' → '3:45p'. Returns '' for None."""
    if not t:
        return ""
    h, m = int(t[:2]), int(t[3:5])
    p = "a" if h < 12 else "p"
    h12 = h % 12 or 12
    return f"{h12}:{m:02d}{p}"


def train_schedule(train):
    """Return dict: location_id → {arrive, depart, note, terminal}."""
    return {
        s["location"]: {
            "arrive": s.get("arrive"),
            "depart": s.get("depart"),
            "note": s.get("note"),
            "terminal": s.get("terminal", False),
        }
        for s in train.get("schedule", [])
    }


def ampm_label(t):
    """'07:10' -> 'A.M.', '15:45' -> 'P.M.'. '' for None."""
    if not t:
        return ""
    return "A.M." if int(t[:2]) < 12 else "P.M."


def col_ampm(stations, sched):
    """Return (first, last) AM/PM labels for a train's schedule, scanning
    stations top-to-bottom (WP->HC). 'first' is the topmost listed time in
    the column, 'last' the bottommost — independent of running direction,
    since NB and SB share the same station row order."""
    first_t = last_t = None
    for st in stations:
        stop = sched.get(st["id"])
        if not stop:
            continue
        t = stop.get("depart") or stop.get("arrive")
        if not t:
            continue
        if first_t is None:
            first_t = t
        last_t = t
    return ampm_label(first_t), ampm_label(last_t)


def time_cell(stop):
    """Return <td> HTML for a schedule stop (or blank if None)."""
    if stop is None:
        return '<td class="time-blank">—</td>'
    arr = fmt12(stop.get("arrive"))
    dep = fmt12(stop.get("depart"))
    note = stop.get("note") or ""
    terminal = stop.get("terminal", False)
    parts = []
    if arr:
        parts.append(f'<div class="arr">{arr}</div>')
    if dep and not terminal:
        parts.append(f'<div class="dep">{dep}</div>')
    if note:
        short = note[:45] + ("…" if len(note) > 45 else "")
        parts.append(f'<div class="note">{_html.escape(short)}</div>')
    if not parts:
        return '<td class="time-blank">—</td>'
    return '<td class="time-cell">' + "".join(parts) + "</td>"


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

CSS = """
* { box-sizing: border-box; }
body {
  font-family: "Times New Roman", Times, serif;
  font-size: 9.5pt;
  margin: 0.5in;
  color: #111;
}
h1 { font-size: 13pt; text-align: center; margin-bottom: 2px; }
.subtitle { font-size: 8.5pt; text-align: center; color: #555; margin-bottom: 6px; }
.rule-note {
  font-size: 7.5pt; color: #7a0000; border: 1px solid #c99;
  padding: 4px 8px; margin-bottom: 8px; background: #fff8f8;
}
table.ett {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 14px;
  font-size: 8.5pt;
}
table.ett th, table.ett td {
  border: 1px solid #aaa;
  padding: 2px 3px;
  vertical-align: middle;
}
/* Direction header */
.dir-nb { background: #dce8f5; text-align: center; font-weight: bold; font-size: 8pt; }
.dir-sb { background: #f5dce8; text-align: center; font-weight: bold; font-size: 8pt; }
/* Class group header */
.cls-hdr { text-align: center; font-size: 7pt; font-weight: bold; letter-spacing: 0.04em; padding: 2px; }
.cls1 { background: #dce8f5; }
.cls2 { background: #e8e8f8; }
.cls3 { background: #e8ead8; }
/* Thick right border marks end of each class group */
td.cls-break, th.cls-break { border-right: 2px solid #666 !important; }
/* AM/PM banner rows */
.ampm-row th, .ampm-row td {
  background: #f0f0ea; text-align: center; font-size: 7pt;
  font-weight: bold; color: #444; padding: 1px 2px;
}
/* Train header cells */
.th-train { background: #eef0f8; text-align: center; vertical-align: bottom; padding: 3px 2px; }
.th-train .tn { font-weight: bold; font-size: 9pt; }
.th-train .ts { font-size: 7pt; color: #555; }
/* Station column */
.st-col { background: #f5f5f0; min-width: 155px; max-width: 190px; }
.st-name { font-weight: bold; font-size: 8.5pt; }
.st-id   { font-size: 7pt; color: #666; }
.st-type { font-size: 7pt; color: #333; }
.st-sid  { font-size: 6.5pt; color: #666; }
.st-flag { color: #8b0000; font-weight: bold; }
.st-sb   { color: #8b0000; font-size: 7.5pt; }
.th-sta  { background: #e8e8e0; text-align: center; font-size: 8pt; font-weight: bold; }
.th-mp   { background: #e8e8e0; text-align: center; font-size: 7pt; font-weight: bold; width: 40px; }
.mp-col  { text-align: center; font-size: 7pt; color: #888; white-space: nowrap; vertical-align: middle; min-width: 36px; }
/* Time cells */
.time-cell { text-align: center; white-space: nowrap; min-width: 36px; }
.time-cell .arr  { font-size: 7.5pt; color: #555; }
.time-cell .dep  { font-size: 8.5pt; }
.time-cell .note { font-size: 6pt; color: #aa0000; line-height: 1.2; }
.time-blank { text-align: center; color: #ccc; font-size: 8pt; }
/* Industry rows */
tr.ind-sub td  { background: #fdfcf8; }
tr.ind-sub .st-col {
  padding-left: 18px; font-size: 7.5pt; color: #666; font-style: italic;
}
tr.ind-onl td { background: #f8f8f4; }
tr.ind-onl .st-col { font-size: 7.5pt; color: #444; }
/* Legend */
.legend { font-size: 7.5pt; color: #555; margin-top: 4px; }
@media print {
  body { font-size: 8.5pt; margin: 0.35in; }
  table.ett { page-break-inside: avoid; }
}
"""

SVC_SHORT = {"Pass": "Pass", "Frght": "Frt", "Coal": "Coal", "Coke": "Coke"}


# ---------------------------------------------------------------------------
# NLS Employee Timetable
# ---------------------------------------------------------------------------

def generate_nls(tt):
    nls = next(s for s in tt["subdivisions"] if s["id"] == "NLS")
    locs_list = nls["locations"]
    locs = {l["id"]: l for l in locs_list}

    # Stations with show_times=True, in milepost order
    stations = sorted(
        [l for l in locs_list if l.get("show_times")],
        key=lambda l: l.get("milepost") or 0,
    )

    # On-line industries: no parent, no show_times, has milepost
    onl_inds = sorted(
        [l for l in locs_list
         if not l.get("show_times") and not l.get("within_limits_of")
         and l.get("milepost") is not None],
        key=lambda l: l.get("milepost") or 0,
    )

    # Sub-industries keyed by parent id
    sub_inds = {}
    for l in locs_list:
        p = l.get("within_limits_of")
        if p and not l.get("show_times"):
            sub_inds.setdefault(p, []).append(l)

    # Build ordered row list, inserting on-line industries by milepost
    rows_plan = []
    oi = 0
    for st in stations:
        st_mp = st.get("milepost") or 0
        while oi < len(onl_inds) and (onl_inds[oi].get("milepost") or 0) < st_mp:
            rows_plan.append(("onl", onl_inds[oi]))
            oi += 1
        rows_plan.append(("sta", st))
        for si in sub_inds.get(st["id"], []):
            rows_plan.append(("sub", si))
    while oi < len(onl_inds):
        rows_plan.append(("onl", onl_inds[oi]))
        oi += 1

    # Trains
    # NB columns sit to the left of the station column, SB to the right.
    # Convention: the fastest/highest-priority class is closest to the
    # station column on both sides — so SB sorts class ascending (Class I
    # first, adjacent to stations) and NB sorts class descending (Class I
    # last, adjacent to stations).
    trains = nls["trains"]
    nb = sorted([t for t in trains if t["direction"] == "N"], key=lambda t: (-t["class"], int(t["number"])))
    sb = sorted([t for t in trains if t["direction"] == "S"], key=lambda t: (t["class"], int(t["number"])))
    nb_s = [train_schedule(t) for t in nb]
    sb_s = [train_schedule(t) for t in sb]

    # Class groups and break positions (index of last column in each class)
    CLS_LABEL = {1: "CLASS I", 2: "CLASS II", 3: "CLASS III"}
    from itertools import groupby as _groupby

    def _class_groups(trains):
        groups = []
        for cls, g in _groupby(trains, key=lambda t: t["class"]):
            groups.append((cls, list(g)))
        return groups

    nb_groups = _class_groups(nb)
    sb_groups = _class_groups(sb)

    # Set of column indices (0-based) that are the LAST in their class group
    def _break_indices(groups):
        idx, breaks = 0, set()
        for _, g in groups:
            idx += len(g)
            breaks.add(idx - 1)
        return breaks

    nb_breaks = _break_indices(nb_groups)
    sb_breaks = _break_indices(sb_groups)

    # Per-column AM/PM banners (top = first listed time, bottom = last)
    nb_ampm = [col_ampm(stations, s) for s in nb_s]
    sb_ampm = [col_ampm(stations, s) for s in sb_s]

    R = []  # HTML rows

    # ── Header ──────────────────────────────────────────────────────────────
    R.append("<thead>")

    # Direction row
    R.append("<tr>")
    R.append(f'<th colspan="{len(nb)}" class="dir-nb">← NORTHWARD</th>')
    R.append('<th class="th-sta">STATIONS</th>')
    R.append('<th class="th-mp">MP</th>')
    R.append(f'<th colspan="{len(sb)}" class="dir-sb">SOUTHWARD →</th>')
    R.append("</tr>")

    # Class grouping row
    R.append("<tr>")
    for cls, group in nb_groups:
        R.append(f'<th colspan="{len(group)}" class="cls-hdr cls{cls} cls-break">{CLS_LABEL[cls]}</th>')
    R.append('<th class="th-sta"></th>')
    R.append('<th class="th-mp"></th>')
    for cls, group in sb_groups:
        R.append(f'<th colspan="{len(group)}" class="cls-hdr cls{cls} cls-break">{CLS_LABEL[cls]}</th>')
    R.append("</tr>")

    # Train number row
    R.append("<tr>")
    for i, t in enumerate(nb):
        brk = ' cls-break' if i in nb_breaks else ''
        R.append(f'<th class="th-train{brk}"><div class="tn">No.{t["number"]}</div>'
                 f'<div class="ts">{SVC_SHORT.get(t["service"], t["service"])}</div></th>')
    R.append('<th class="th-sta"></th>')
    R.append('<th class="th-mp"></th>')
    for i, t in enumerate(sb):
        brk = ' cls-break' if i in sb_breaks else ''
        R.append(f'<th class="th-train{brk}"><div class="tn">No.{t["number"]}</div>'
                 f'<div class="ts">{SVC_SHORT.get(t["service"], t["service"])}</div></th>')
    R.append("</tr>")

    # AM/PM top banner — first listed time per column
    R.append('<tr class="ampm-row">')
    for i, t in enumerate(nb):
        brk = ' cls-break' if i in nb_breaks else ''
        R.append(f'<th class="ampm-cell{brk}">{nb_ampm[i][0]}</th>')
    R.append('<th class="th-sta"></th>')
    R.append('<th class="th-mp"></th>')
    for i, t in enumerate(sb):
        brk = ' cls-break' if i in sb_breaks else ''
        R.append(f'<th class="ampm-cell{brk}">{sb_ampm[i][0]}</th>')
    R.append("</tr>")

    R.append("</thead><tbody>")

    # ── Body rows ────────────────────────────────────────────────────────────
    for kind, loc in rows_plan:
        loc_id = loc["id"]

        if kind == "sta":
            R.append("<tr>")
            for i, t in enumerate(nb):
                cell = time_cell(nb_s[i].get(loc_id))
                if i in nb_breaks:
                    cell = cell.replace('class="time-blank"', 'class="time-blank cls-break"', 1).replace('class="time-cell"', 'class="time-cell cls-break"', 1)
                R.append(cell)
            # Station cell
            name = loc.get("name", loc_id)
            types_str = " · ".join(x for x in loc.get("types", []) if x != "I")
            mp = loc.get("milepost")
            mp_exit = loc.get("milepost_exit")
            siding = loc.get("siding_length_cars")
            flagged = loc.get("flagging_required", False)
            switchback = loc.get("switchback", False)
            mp_val = f"{mp:.1f}" if mp is not None else ""
            if mp_exit:
                mp_val += f"–{mp_exit:.1f}"
            inner = f'<div class="st-name">{_html.escape(name)}'
            if flagged:
                inner += ' <span class="st-flag">F</span>'
            if switchback:
                inner += ' <span class="st-sb">↺</span>'
            inner += "</div>"
            if types_str:
                inner += f'<div class="st-type">{types_str}</div>'
            if siding:
                inner += f'<div class="st-sid">Siding {siding} cars</div>'
            R.append(f'<td class="st-col">{inner}</td>')
            R.append(f'<td class="mp-col">{mp_val}</td>')
            for i, t in enumerate(sb):
                cell = time_cell(sb_s[i].get(loc_id))
                if i in sb_breaks:
                    cell = cell.replace('class="time-blank"', 'class="time-blank cls-break"', 1).replace('class="time-cell"', 'class="time-cell cls-break"', 1)
                R.append(cell)
            R.append("</tr>")

        elif kind == "sub":
            R.append('<tr class="ind-sub">')
            for _ in nb:
                R.append("<td></td>")
            name = loc.get("name", loc_id)
            spots = loc.get("car_spots", "?")
            sb_mark = " ↺" if loc.get("switchback") else ""
            R.append(f'<td class="st-col">↳ {_html.escape(name)}{sb_mark} · {spots} spots</td>')
            R.append('<td class="mp-col"></td>')
            for _ in sb:
                R.append("<td></td>")
            R.append("</tr>")

        elif kind == "onl":
            R.append('<tr class="ind-onl">')
            for _ in nb:
                R.append("<td></td>")
            name = loc.get("name", loc_id)
            spots = loc.get("car_spots", "?")
            mp = loc.get("milepost")
            mp_val = f"{mp:.1f}" if mp is not None else ""
            sb_mark = " ↺" if loc.get("switchback") else ""
            R.append(f'<td class="st-col">{_html.escape(name)}{sb_mark} · {spots} spots</td>')
            R.append(f'<td class="mp-col">{mp_val}</td>')
            for _ in sb:
                R.append("<td></td>")
            R.append("</tr>")

    # AM/PM bottom banner — last listed time per column
    R.append('<tr class="ampm-row">')
    for i, t in enumerate(nb):
        brk = ' cls-break' if i in nb_breaks else ''
        R.append(f'<td class="ampm-cell{brk}">{nb_ampm[i][1]}</td>')
    R.append('<td class="st-col"></td>')
    R.append('<td class="mp-col"></td>')
    for i, t in enumerate(sb):
        brk = ' cls-break' if i in sb_breaks else ''
        R.append(f'<td class="ampm-cell{brk}">{sb_ampm[i][1]}</td>')
    R.append("</tr>")

    R.append("</tbody>")

    # ── Assemble ─────────────────────────────────────────────────────────────
    tt_meta = tt.get("timetable", {})
    notes = tt_meta.get("notes", [])
    notes_html = ""
    if notes:
        notes_html = ('<div class="rule-note"><strong>Special instructions:</strong> '
                      + " &nbsp;|&nbsp; ".join(_html.escape(n) for n in notes)
                      + "</div>")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>NY&amp;E Timetable No.{tt_meta.get('number','4')} — NLS Employee Timetable</title>
<style>{CSS}</style>
</head>
<body>
<h1>New York and Eastern Railroad</h1>
<div class="subtitle">Northern Lights Subdivision &nbsp;·&nbsp; Employee Timetable No.{tt_meta.get('number','4')} &nbsp;·&nbsp; Effective {tt_meta.get('effective','')}</div>
<div class="subtitle">Southward trains superior by direction &nbsp;·&nbsp; All times Railroad Time &nbsp;·&nbsp; a=AM &nbsp; p=PM</div>
{notes_html}
<table class="ett">
{"".join(R)}
</table>
<p class="legend">F = Flagging required &nbsp;|&nbsp; ↺ = Reversing station or spur &nbsp;|&nbsp; TO = Train Order telegraph &nbsp;|&nbsp; R = Register station &nbsp;|&nbsp; YL = Yard limits</p>
</body>
</html>"""


# ---------------------------------------------------------------------------
# C&O Reference Table
# ---------------------------------------------------------------------------

def generate_coe(tt):
    coe = next(s for s in tt["subdivisions"] if s["id"] == "COE")
    trains = coe["trains"]

    svc_long = {"Pass": "Passenger", "Coal": "Coal", "Frght": "Freight"}
    dir_label = {"W": "→ West (Covington WV)", "E": "← East (Cumberland MD)"}

    # Sort by WP depart or arrive time
    def wp_time(t):
        for s in t.get("schedule", []):
            if s["location"] in ("WP_COE",):
                return s.get("depart") or s.get("arrive") or "99:99"
        return "99:99"

    sorted_trains = sorted(trains, key=wp_time)

    rows = ["<tbody>"]
    for t in sorted_trains:
        sched = train_schedule(t)
        wp = sched.get("WP_COE", {})
        arr = fmt12(wp.get("arrive"))
        dep = fmt12(wp.get("depart"))
        direction = dir_label.get(t["direction"], t["direction"])
        svc = svc_long.get(t["service"], t["service"])
        cls = f"Class {t['class']}"
        rows.append(
            f"<tr>"
            f"<td style='text-align:center;font-weight:bold'>No.{t['number']}</td>"
            f"<td>{svc}</td><td>{cls}</td><td>{direction}</td>"
            f"<td style='text-align:center'>{arr}</td>"
            f"<td style='text-align:center'>{dep}</td>"
            f"</tr>"
        )
    rows.append("</tbody>")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>C&amp;O East Central — WP Passing Times</title>
<style>
{CSS}
table.coe {{ border-collapse: collapse; margin-bottom: 12px; }}
table.coe th, table.coe td {{ border: 1px solid #aaa; padding: 3px 8px; font-size: 9pt; }}
table.coe th {{ background: #dce8f5; text-align: center; }}
</style>
</head>
<body>
<h1>C&amp;O East Central Subdivision</h1>
<div class="subtitle">Williamsport (WP) Passing Times — Yardmaster Reference</div>
<table class="coe">
<thead>
<tr><th>Train</th><th>Service</th><th>Class</th><th>Direction</th><th>WP Arrive</th><th>WP Depart</th></tr>
</thead>
{"".join(rows)}
</table>
<p class="legend">All times Railroad Time (a=AM, p=PM). Full schedule: Timetable No.{tt.get('timetable',{}).get('number','4')}.</p>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    with open(DATA) as f:
        tt = json.load(f)

    nls_html = generate_nls(tt)
    OUT_NLS.write_text(nls_html, encoding="utf-8")
    print(f"Written: {OUT_NLS}")

    coe_html = generate_coe(tt)
    OUT_COE.write_text(coe_html, encoding="utf-8")
    print(f"Written: {OUT_COE}")
