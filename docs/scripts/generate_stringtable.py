#!/usr/bin/env python3
"""
generate_stringtable.py  —  NY&E Timetable No. 4  string table (time-distance diagram)

Layout (Option B):
  X = milepost   (WP mp=0 at left  →  HC mp=135 at right)
  Y = railroad time  (00:00 at top  →  24:00 at bottom)

C&O interchange trains shown as vertical marks at mp=0 (WP) with
direction stubs indicating westbound/eastbound.

Dwell line weight:
  Bold  = active work  (passenger boarding, setout/pickup, WP_YARD)
  Thin  = schedule wait  (meet hold, switchback swap, gap)

Mine spur: horizontal dashed stub from station MP to industry MP at dwell midpoint.

XP (long siding, mp 37–43.5): dwell shown as diagonal across the siding.

Usage:
  python3 generate_stringtable.py
Output:
  Trains/docs/NYE_StringTable.svg
"""

import json
import re
from pathlib import Path

# ── paths ─────────────────────────────────────────────────────────────────────
HERE      = Path(__file__).parent
TIMETABLE = HERE.parent.parent / "IOTtrains" / "RR_Server" / "data" / "timetable.json"
OUTPUT    = HERE.parent / "NYE_StringTable.svg"

# ── colour palette ────────────────────────────────────────────────────────────
SVC_CLR = {
    "Pass":  "#1565c0",   # deep blue
    "Coal":  "#212121",   # near-black
    "Frght": "#bf360c",   # deep orange-red
    "Coke":  "#5d4037",   # dark brown
}
COE_CLR = {
    "Pass":  "#1976d2",   # mid-blue
    "Coal":  "#9e9e9e",   # grey
    "Frght": "#e64a19",   # orange
}
MEET_CLR  = "#c62828"     # red meet dot
GRID_MJ   = "#d0d0d0"     # major grid (6h)
GRID_MD   = "#e4e4e4"     # medium grid (3h)
GRID_MN   = "#f2f2f2"     # minor grid (1h)
STN_LINE  = "#c0c0c0"     # station vertical guide
XP_EXIT   = "#bbddbb"     # XP north-switch guide (dashed)
IND_TICK  = "#dddddd"     # industry tick
COE_BG    = "#eaf3fb"
BG        = "#ffffff"
LBL_FG    = "#666666"
TITLE_FG  = "#1a1a1a"

# ── layout ────────────────────────────────────────────────────────────────────
PX_MI  = 4.5     # px per model-mile  →  plot width  = 135 × 4.5 = 607.5 px
PX_HR  = 40.0    # px per hour        →  plot height = 24  × 40  = 960   px
PAD_L  = 54      # time-axis labels (left)
PAD_R  = 106     # legend (right)
PAD_T  = 86      # station headers (top)
PAD_B  = 36
COE_H  = 68      # C&O reference band height above main plot

# ── line weights ──────────────────────────────────────────────────────────────
W_TRAVEL = 1.5
W_BOLD   = 3.5   # active-work dwell
W_THIN   = 1.5   # schedule-wait dwell
W_SPUR   = 1.5   # mine spur dashed stub
DASH_SP  = "4,3"
W_COE    = 4.0   # C&O dwell mark
COE_STUB = 18    # direction-stub px

# ── helpers ───────────────────────────────────────────────────────────────────
def t2m(t):
    """'HH:MM' → minutes since midnight, or None."""
    if not t:
        return None
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def is_active(loc_id, note, svc):
    """True → bold dwell (active work).  False → thin dwell (schedule wait)."""
    n = (note or "").lower()
    if "setout" in n or "pickup" in n:
        return True
    if svc == "Pass" and loc_id not in ("WP_EAST_STG", "WP_WEST_STG"):
        return True
    if loc_id in ("WP_YARD", "WP"):
        return True
    return False


def meet_no(note):
    m = re.search(r"[Ww]ait for [Nn]o\.?\s*(\d+)", note or "")
    return m.group(1) if m else None


# ── SVG builder ───────────────────────────────────────────────────────────────
class SVG:
    def __init__(self):
        self._e = []

    def __iadd__(self, s):
        self._e.append(s)
        return self

    def line(self, x1, y1, x2, y2, stroke, sw, dash="", opacity=1.0):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        op = f' opacity="{opacity:.2f}"' if opacity < 1.0 else ""
        self += (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{da}{op}/>')

    def circle(self, cx, cy, r, fill, stroke="none", sw=1):
        self += (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def rect(self, x, y, w, h, fill, stroke="none", sw=0, rx=0):
        self += (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" rx="{rx}"/>')

    @staticmethod
    def _esc(s):
        return (s.replace("&", "&amp;")
                 .replace("<", "&lt;")
                 .replace(">", "&gt;"))

    def text(self, tx, ty, s, anchor="middle", size=10, weight="normal",
             fill=LBL_FG, rotate=0):
        rot = f' transform="rotate({rotate},{tx:.1f},{ty:.1f})"' if rotate else ""
        self += (f'<text x="{tx:.1f}" y="{ty:.1f}" '
                 f'font-family="Arial,Helvetica,sans-serif" '
                 f'font-size="{size}" text-anchor="{anchor}" '
                 f'fill="{fill}" font-weight="{weight}"{rot}>{self._esc(s)}</text>')

    def render(self, w, h):
        hdr = (f'<?xml version="1.0" encoding="UTF-8"?>\n'
               f'<svg xmlns="http://www.w3.org/2000/svg" '
               f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n')
        return hdr + "\n".join(self._e) + "\n</svg>"


# ── main generator ────────────────────────────────────────────────────────────
def generate():
    data = json.loads(TIMETABLE.read_text())
    nls  = next(s for s in data["subdivisions"] if s["id"] == "NLS")
    coe  = next(s for s in data["subdivisions"] if s["id"] == "COE")
    locs = {l["id"]: l for l in nls["locations"]}

    # ── canvas ────────────────────────────────────────────────────────────────
    plot_left = PAD_L
    plot_top  = PAD_T + COE_H
    plot_w    = 135 * PX_MI       # 607.5 px
    plot_h    = 24  * PX_HR       # 960   px

    total_w = int(plot_left + plot_w + PAD_R)
    total_h = int(plot_top  + plot_h + PAD_B)

    def X(mp):  return plot_left + mp * PX_MI
    def Y(mn):  return plot_top  + (mn / 60.0) * PX_HR

    svg = SVG()

    # ── backgrounds ───────────────────────────────────────────────────────────
    svg.rect(0, 0, total_w, total_h, BG)
    svg.rect(plot_left, PAD_T, plot_w, COE_H, COE_BG)
    svg += (f'<rect x="{plot_left:.1f}" y="{PAD_T}" '
            f'width="{plot_w:.1f}" height="{COE_H}" '
            f'fill="none" stroke="#aaccee" stroke-width="0.8"/>')
    svg.rect(plot_left, plot_top, plot_w, plot_h, "#fafafa",
             stroke="#cccccc", sw=0.5)

    # ── hour grid ─────────────────────────────────────────────────────────────
    for hr in range(25):
        yy = Y(hr * 60)
        if   hr % 6 == 0: clr, sw = GRID_MJ, 0.9
        elif hr % 3 == 0: clr, sw = GRID_MD, 0.6
        else:              clr, sw = GRID_MN, 0.4
        svg.line(plot_left, yy, plot_left + plot_w, yy, clr, sw)

    # ── classify locations ────────────────────────────────────────────────────
    guide = [l for l in nls["locations"]
             if l.get("show_times") and l.get("milepost") is not None]
    minor = [l for l in nls["locations"]
             if not l.get("show_times")
             and l.get("milepost") is not None
             and not l.get("within_limits_of")]

    # ── station vertical guides + headers ─────────────────────────────────────
    for loc in guide:
        xp = X(loc["milepost"])
        svg.line(xp, plot_top, xp, plot_top + plot_h, STN_LINE, 0.7)
        svg.line(xp, PAD_T,    xp, plot_top,          STN_LINE, 0.4, dash="2,4")
        # switchback marker (small triangle at plot top)
        if loc.get("switchback"):
            pts = f"{xp:.1f},{plot_top} {xp-4:.1f},{plot_top-7} {xp+4:.1f},{plot_top-7}"
            svg += f'<polygon points="{pts}" fill="{SVC_CLR["Coal"]}" opacity="0.35"/>'
        # rotated label
        ly = PAD_T - 8
        svg.text(xp + 2, ly, loc["id"], anchor="start", size=10,
                 weight="bold", fill=TITLE_FG, rotate=-55)
        mp_lbl = f"mp {loc['milepost']:.0f}"
        if loc.get("milepost_exit"):
            mp_lbl += f"–{loc['milepost_exit']:.0f}"
        svg.text(xp + 2, ly + 14, mp_lbl, anchor="start", size=7,
                 fill=LBL_FG, rotate=-55)

    # XP north-switch guide (dashed)
    svg.line(X(43.5), plot_top, X(43.5), plot_top + plot_h,
             XP_EXIT, 0.6, dash="3,6")

    # minor stops — short tick + small label
    for loc in minor:
        xp = X(loc["milepost"])
        svg.line(xp, plot_top, xp, plot_top + 12, IND_TICK, 0.6)
        svg.text(xp + 2, PAD_T - 4, loc["id"], anchor="start",
                 size=7, fill="#aaaaaa", rotate=-55)

    # ── time axis ─────────────────────────────────────────────────────────────
    for hr in range(25):
        yy = Y(hr * 60)
        if hr % 3 == 0:
            svg.text(plot_left - 4, yy + 3.5, f"{hr:02d}:00",
                     anchor="end", size=9, fill=LBL_FG)
        else:
            svg.text(plot_left - 4, yy + 3.5, f"{hr:02d}",
                     anchor="end", size=7, fill="#aaaaaa")

    # ── titles + axis labels ──────────────────────────────────────────────────
    mx = plot_left + plot_w / 2
    svg.text(mx, 15,
             "NY&E Northern Lights Subdivision — Timetable No. 4 — String Table",
             size=12, weight="bold", fill=TITLE_FG)
    svg.text(mx, 30,
             "X = Milepost (WP mp 0 → HC mp 135)  ·  "
             "Y = Railroad time  ·  Southward trains superior by direction",
             size=9, fill=LBL_FG)
    svg.text(plot_left - 4, plot_top - 5, "RR time",
             anchor="end", size=8, fill=LBL_FG)

    # ── C&O band header ───────────────────────────────────────────────────────
    svg.text(4, PAD_T + 16, "C&O", anchor="start", size=9,
             weight="bold", fill="#1565c0")
    svg.text(4, PAD_T + 28, "East Central", anchor="start", size=7, fill=LBL_FG)
    svg.text(plot_left + 6, PAD_T + 20,
             "← W.Covington WV  ·  WP (mp 0)  ·  E.Cumberland MD →",
             anchor="start", size=8, fill="#1565c0")

    # ── NLS trains ────────────────────────────────────────────────────────────
    for train in nls["trains"]:
        svc   = train["service"]
        clr   = SVC_CLR.get(svc, "#888888")
        dirn  = train["direction"]  # "N" or "S"
        num   = train["number"]

        stops = []
        for entry in train["schedule"]:
            lid = entry["location"]
            loc = locs.get(lid)
            if loc is None:
                continue
            mp = loc.get("milepost")
            if mp is None:
                pid = loc.get("within_limits_of")
                mp  = locs[pid]["milepost"] if pid and locs.get(pid) else None
            if mp is None:
                continue
            stops.append({
                "mp":   mp,
                "loc":  loc,
                "lid":  lid,
                "arr":  t2m(entry.get("arrive")),
                "dep":  t2m(entry.get("depart")),
                "note": entry.get("note", ""),
            })

        if not stops:
            continue

        prev_mp = None
        prev_t  = None   # time train LEFT previous station

        for s in stops:
            mp, loc = s["mp"], s["loc"]
            arr, dep, lid, note = s["arr"], s["dep"], s["lid"], s["note"]

            t_arr  = arr if arr is not None else dep
            t_dep  = dep if dep is not None else arr

            # ── arrival MP and departure MP (handles long sidings like XP) ──
            mp_exit = loc.get("milepost_exit")
            if mp_exit:
                arr_mp = mp       if dirn == "N" else mp_exit
                dep_mp = mp_exit  if dirn == "N" else mp
            else:
                arr_mp = dep_mp = mp

            # travel diagonal from previous stop
            if prev_t is not None and prev_mp is not None:
                svg.line(X(prev_mp), Y(prev_t), X(arr_mp), Y(t_arr),
                         clr, W_TRAVEL)

            # dwell
            if arr is not None and dep is not None and dep > arr:
                sw = W_BOLD if is_active(lid, note, svc) else W_THIN
                if mp_exit:
                    # long siding: diagonal across the siding length
                    svg.line(X(arr_mp), Y(arr), X(dep_mp), Y(dep), clr, sw)
                else:
                    # regular station: vertical mark
                    svg.line(X(mp), Y(arr), X(mp), Y(dep), clr, sw)

                # mine spur dashed stub
                n = note.lower()
                if "setout" in n or "pickup" in n:
                    spur_list = [l for l in nls["locations"]
                                 if l.get("within_limits_of") == lid
                                 and l.get("milepost") is not None]
                    mid_t = (arr + dep) / 2.0
                    for sl in spur_list:
                        svg.line(X(mp), Y(mid_t), X(sl["milepost"]), Y(mid_t),
                                 clr, W_SPUR, dash=DASH_SP)
                        svg.text(X(sl["milepost"]) + 2, Y(mid_t) - 2,
                                 sl["id"], anchor="start", size=7, fill=clr)

            # meet dot
            if meet_no(note):
                dot_y = Y(t_arr if t_arr is not None else t_dep)
                svg.circle(X(arr_mp), dot_y, 3.5, MEET_CLR, stroke="white", sw=0.8)

            prev_mp = dep_mp
            prev_t  = t_dep

        # train number label near first stop
        if stops:
            s0 = stops[0]
            t0 = s0["dep"] if s0["dep"] is not None else s0["arr"]
            if t0 is not None:
                ox  = 4  if dirn == "N" else -4
                anc = "start" if dirn == "N" else "end"
                svg.text(X(s0["mp"]) + ox, Y(t0) - 3, num,
                         anchor=anc, size=8, weight="bold", fill=clr)

    # ── C&O trains ── vertical marks at mp=0 with direction stubs ─────────────
    # Westbound offset slightly left, eastbound slightly right to avoid overlap
    coe_offsets = {"W": -4.5, "E": 4.5}

    for train in coe["trains"]:
        svc   = train["service"]
        clr   = COE_CLR.get(svc, "#888888")
        dirn  = train["direction"]   # "W" or "E"
        num   = train["number"]
        xoff  = coe_offsets.get(dirn, 0)
        cx    = X(0) + xoff

        for entry in train["schedule"]:
            if entry["location"] != "WP_COE":
                continue
            arr  = t2m(entry.get("arrive"))
            dep  = t2m(entry.get("depart"))
            note = entry.get("note", "")
            t_a  = arr if arr is not None else dep
            t_d  = dep if dep is not None else arr
            if t_a is None:
                continue

            # main-plot dwell mark
            y1 = Y(t_a)
            y2 = Y(t_d) if (t_d is not None and t_d > t_a) else y1 + 8
            svg.line(cx, y1, cx, y2, clr, W_COE)

            # direction stub (shows which way the train is heading)
            stub_x = cx - COE_STUB if dirn == "W" else cx + COE_STUB
            svg.line(cx, (y1 + y2) / 2, stub_x, (y1 + y2) / 2,
                     clr, W_TRAVEL, dash="3,3")

            # compressed marker in C&O band (same colour, 3px wide)
            by1 = PAD_T + (t_a / 1440.0) * COE_H
            by2 = PAD_T + (t_d / 1440.0) * COE_H if t_d else by1 + 4
            svg.line(cx, by1, cx, max(by2, by1 + 3), clr, 3.0)

            # label
            lx  = cx + (7 if dirn == "E" else -7)
            anc = "start" if dirn == "E" else "end"
            svg.text(lx, y1 - 3, f"C&O {num}",
                     anchor=anc, size=7, weight="bold", fill=clr)

    # ── legend ────────────────────────────────────────────────────────────────
    lx = int(plot_left + plot_w) + 10
    ly = plot_top + 18

    svg.text(lx, ly - 8, "Legend", anchor="start", size=10,
             weight="bold", fill=TITLE_FG)

    # train types
    for i, (lbl, clr) in enumerate([
        ("Passenger",    SVC_CLR["Pass"]),
        ("Coal",         SVC_CLR["Coal"]),
        ("Freight/Coke", SVC_CLR["Frght"]),
    ]):
        y0 = ly + i * 20
        svg.line(lx, y0 + 5, lx + 22, y0 + 5, clr, W_TRAVEL + 0.5)
        svg.text(lx + 26, y0 + 8, lbl, anchor="start", size=9, fill=LBL_FG)

    ly += 76

    svg.text(lx, ly, "Dwell:", anchor="start", size=9,
             weight="bold", fill=TITLE_FG)
    ly += 14
    svg.line(lx, ly + 4, lx + 22, ly + 4, "#555555", W_BOLD)
    svg.text(lx + 26, ly + 7, "Active work", anchor="start", size=9, fill=LBL_FG)
    ly += 17
    svg.line(lx, ly + 4, lx + 22, ly + 4, "#555555", W_THIN)
    svg.text(lx + 26, ly + 7, "Schedule wait", anchor="start", size=9, fill=LBL_FG)
    ly += 24

    svg.text(lx, ly, "Marks:", anchor="start", size=9,
             weight="bold", fill=TITLE_FG)
    ly += 14
    svg.line(lx, ly + 4, lx + 22, ly + 4, "#555555", W_SPUR, dash=DASH_SP)
    svg.text(lx + 26, ly + 7, "Mine spur work", anchor="start", size=9, fill=LBL_FG)
    ly += 17
    svg.circle(lx + 11, ly + 4, 3.5, MEET_CLR, stroke="white", sw=0.8)
    svg.text(lx + 26, ly + 7, "Meet point", anchor="start", size=9, fill=LBL_FG)
    ly += 24

    svg.text(lx, ly, "C&O:", anchor="start", size=9,
             weight="bold", fill=TITLE_FG)
    ly += 14
    svg.line(lx, ly + 4, lx + 11, ly + 4, COE_CLR["Coal"], W_COE)
    svg.line(lx + 11, ly + 4, lx + 22, ly + 4,
             COE_CLR["Coal"], W_TRAVEL, dash="3,3")
    svg.text(lx + 26, ly + 7, "At WP (bold=dwell)", anchor="start",
             size=9, fill=LBL_FG)

    # switchback symbol key
    ly += 24
    svg.text(lx, ly, "Station types:", anchor="start", size=9,
             weight="bold", fill=TITLE_FG)
    ly += 14
    xk = lx + 11
    pts = f"{xk:.1f},{ly} {xk-4:.1f},{ly-7} {xk+4:.1f},{ly-7}"
    svg += f'<polygon points="{pts}" fill="{SVC_CLR["Coal"]}" opacity="0.35"/>'
    svg.text(lx + 26, ly, "▲ Switchback", anchor="start", size=9, fill=LBL_FG)
    ly += 14
    svg.line(lx + 4, ly + 4, lx + 18, ly + 4, XP_EXIT, 1.2, dash="3,6")
    svg.text(lx + 26, ly + 7, "Long siding exit", anchor="start", size=9, fill=LBL_FG)

    # ── write output ──────────────────────────────────────────────────────────
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg.render(total_w, total_h))
    print(f"Written: {OUTPUT}  ({total_w} × {total_h} px)")


if __name__ == "__main__":
    generate()
