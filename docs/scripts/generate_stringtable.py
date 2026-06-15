#!/usr/bin/env python3
"""
generate_stringtable.py  —  NY&E Timetable No. 4  string table (time-distance diagram)

Layout:
  Left strip : C&O East Central — two sub-columns (West / East) at WP
  WP_YARD    : dedicated sub-column, left of main plot
  Main plot  : X = milepost (WP mp 0 → HC mp 208)  Y = railroad time (00:00 top)
"""

import json
import re
from pathlib import Path

HERE      = Path(__file__).parent
TIMETABLE = HERE.parent.parent / "IOTtrains" / "RR_Server" / "data" / "timetable.json"
OUTPUT    = HERE.parent / "NYE_StringTable.svg"

# ── colour palette ─────────────────────────────────────────────────────────────
SVC_CLR = {
    "Pass":  "#1565c0",   # deep blue
    "Coal":  "#212121",   # near-black
    "Coke":  "#212121",   # same as Coal — class 3, runs identically
    "Frght": "#bf360c",   # deep orange-red
}
EXPRESS_CLR = "#2e7d32"   # Train 11 — express freight (distinct from regular Frght)

COE_CLR = {
    "Pass":  "#1976d2",
    "Coal":  "#9e9e9e",
    "Frght": "#e64a19",
}

MEET_CLR  = "#c62828"
GRID_MJ   = "#d0d0d0"
GRID_MD   = "#e4e4e4"
GRID_MN   = "#f2f2f2"
STN_LINE  = "#c0c0c0"
XP_EXIT   = "#bbddbb"
IND_TICK  = "#dddddd"
BG        = "#ffffff"
LBL_FG    = "#666666"
TITLE_FG  = "#1a1a1a"
COE_BG    = "#eaf3fb"
WY_BG     = "#f5f5f0"   # WP_YARD sub-column background

# ── layout ────────────────────────────────────────────────────────────────────
TARGET_PLOT_W = 607.5   # main NLS plot width (px); PX_MI auto-computed
PX_HR   = 40.0          # px per hour  →  24 × 40 = 960 px tall
PAD_L   = 54            # time-axis labels (left of C&O strip)
PAD_R   = 110           # legend (right)
PAD_T   = 86            # station headers (top)
PAD_B   = 36

# C&O left strip
COE_STRIP_W  = 56       # px width of C&O strip (between PAD_L and WP_YARD)
COE_W_OFF    = 10       # westbound col centre offset within strip
COE_E_OFF    = 42       # eastbound col centre offset within strip

# WP_YARD sub-column (between C&O strip and main plot)
WP_YARD_W    = 28       # px width of WP_YARD area
WP_YARD_MID  = 14       # centre offset within WP_YARD area
SECTION_SEP  = 6        # gap between WP_YARD area and plot_left (WP)

# ── line weights ───────────────────────────────────────────────────────────────
W_TRAVEL = 1.5
W_BOLD   = 3.5
W_THIN   = 1.5
W_SPUR   = 1.5
DASH_SP  = "4,3"


# ── helpers ───────────────────────────────────────────────────────────────────
def t2m(t):
    if not t:
        return None
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def is_active(loc_id, note, svc):
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
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

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


# ── main generator ─────────────────────────────────────────────────────────────
def generate():
    data = json.loads(TIMETABLE.read_text())
    nls  = next(s for s in data["subdivisions"] if s["id"] == "NLS")
    coe  = next(s for s in data["subdivisions"] if s["id"] == "COE")
    locs = {l["id"]: l for l in nls["locations"]}

    # ── derived geometry ──────────────────────────────────────────────────────
    mp_max = max(
        (l["milepost"] for l in nls["locations"]
         if l.get("show_times") and l.get("milepost") is not None),
        default=208,
    )
    PX_MI = TARGET_PLOT_W / mp_max

    coe_w_x   = PAD_L + COE_W_OFF
    coe_e_x   = PAD_L + COE_E_OFF
    wp_yard_x = PAD_L + COE_STRIP_W + WP_YARD_MID
    plot_left  = PAD_L + COE_STRIP_W + WP_YARD_W + SECTION_SEP   # X for mp=0 (WP)
    plot_top   = PAD_T
    plot_w     = TARGET_PLOT_W
    plot_h     = 24 * PX_HR   # 960 px

    total_w = int(plot_left + plot_w + PAD_R)
    total_h = int(plot_top  + plot_h + PAD_B)

    def X(mp):
        return plot_left + mp * PX_MI

    def Y(mn):
        return plot_top + (mn / 60.0) * PX_HR

    def stop_x(lid, mp, mp_exit, dirn, which):
        """Pixel X for a stop's arrival or departure side."""
        if lid == "WP_YARD":
            return wp_yard_x
        if mp_exit:
            raw = (mp if dirn == "N" else mp_exit) if which == "arr" \
                  else (mp_exit if dirn == "N" else mp)
        else:
            raw = mp
        return X(raw if raw is not None else mp)

    svg = SVG()

    # ── backgrounds ───────────────────────────────────────────────────────────
    svg.rect(0, 0, total_w, total_h, BG)
    # C&O strip
    svg.rect(PAD_L, plot_top, COE_STRIP_W, plot_h, COE_BG,
             stroke="#aaccee", sw=0.8)
    # WP_YARD area
    svg.rect(PAD_L + COE_STRIP_W, plot_top, WP_YARD_W + SECTION_SEP, plot_h,
             WY_BG, stroke="#cccccc", sw=0.5)
    # Main NLS plot
    svg.rect(plot_left, plot_top, plot_w, plot_h, "#fafafa",
             stroke="#cccccc", sw=0.5)

    # ── hour grid (spans from C&O strip left edge to plot right edge) ─────────
    for hr in range(25):
        yy = Y(hr * 60)
        if   hr % 6 == 0: clr, sw = GRID_MJ, 0.9
        elif hr % 3 == 0: clr, sw = GRID_MD, 0.6
        else:              clr, sw = GRID_MN, 0.4
        svg.line(PAD_L, yy, plot_left + plot_w, yy, clr, sw)

    # ── classify NLS locations ────────────────────────────────────────────────
    guide = [l for l in nls["locations"]
             if l.get("show_times") and l.get("milepost") is not None]
    minor = [l for l in nls["locations"]
             if not l.get("show_times")
             and l.get("milepost") is not None
             and not l.get("within_limits_of")]

    # ── station vertical guides + rotated headers ─────────────────────────────
    for loc in guide:
        lid = loc["id"]
        if lid == "WP_YARD":
            continue   # drawn separately below
        xp = X(loc["milepost"])
        svg.line(xp, plot_top, xp, plot_top + plot_h, STN_LINE, 0.7)
        if loc.get("switchback"):
            pts = (f"{xp:.1f},{plot_top} {xp-4:.1f},{plot_top-7} "
                   f"{xp+4:.1f},{plot_top-7}")
            svg += f'<polygon points="{pts}" fill="{SVC_CLR["Coal"]}" opacity="0.35"/>'
        ly = PAD_T - 8
        svg.text(xp + 2, ly, lid, anchor="start", size=10,
                 weight="bold", fill=TITLE_FG, rotate=-55)
        mp_lbl = f"mp {loc['milepost']:.0f}"
        if loc.get("milepost_exit"):
            mp_lbl += f"–{loc['milepost_exit']:.0f}"
        svg.text(xp + 2, ly + 14, mp_lbl, anchor="start", size=7,
                 fill=LBL_FG, rotate=-55)

    # WP_YARD guide + header
    svg.line(wp_yard_x, plot_top, wp_yard_x, plot_top + plot_h, STN_LINE, 1.0)
    ly = PAD_T - 8
    svg.text(wp_yard_x + 2, ly, "WP_YARD", anchor="start", size=10,
             weight="bold", fill=TITLE_FG, rotate=-55)
    svg.text(wp_yard_x + 2, ly + 14, "mp 0", anchor="start", size=7,
             fill=LBL_FG, rotate=-55)

    # Long-siding exit guides (dashed) — XP and any future long sidings
    for loc in guide:
        if (loc.get("milepost_exit") and loc.get("show_both_times")
                and not loc.get("switchback")):
            svg.line(X(loc["milepost_exit"]), plot_top,
                     X(loc["milepost_exit"]), plot_top + plot_h,
                     XP_EXIT, 0.6, dash="3,6")

    # Minor stops (on-line industries) — short tick + small label
    for loc in minor:
        xp = X(loc["milepost"])
        svg.line(xp, plot_top, xp, plot_top + 12, IND_TICK, 0.6)
        svg.text(xp + 2, PAD_T - 4, loc["id"], anchor="start",
                 size=7, fill="#aaaaaa", rotate=-55)

    # ── C&O strip headers ─────────────────────────────────────────────────────
    mid_coe = PAD_L + COE_STRIP_W // 2
    svg.line(mid_coe, plot_top, mid_coe, plot_top + plot_h, "#aaccee", 0.5)
    svg.text(coe_w_x, PAD_T - 22, "C&O", anchor="middle",
             size=8, weight="bold", fill="#1565c0")
    svg.text(coe_w_x, PAD_T - 11, "West", anchor="middle", size=7, fill=LBL_FG)
    svg.text(coe_e_x, PAD_T - 22, "C&O", anchor="middle",
             size=8, weight="bold", fill="#1565c0")
    svg.text(coe_e_x, PAD_T - 11, "East", anchor="middle", size=7, fill=LBL_FG)

    # ── time axis ─────────────────────────────────────────────────────────────
    for hr in range(25):
        yy = Y(hr * 60)
        if hr % 3 == 0:
            svg.text(PAD_L - 4, yy + 3.5, f"{hr:02d}:00",
                     anchor="end", size=9, fill=LBL_FG)
        else:
            svg.text(PAD_L - 4, yy + 3.5, f"{hr:02d}",
                     anchor="end", size=7, fill="#aaaaaa")

    # ── titles ────────────────────────────────────────────────────────────────
    mx = plot_left + plot_w / 2
    svg.text(mx, 15,
             "NY&E Northern Lights Subdivision — Timetable No. 4 — String Table",
             size=12, weight="bold", fill=TITLE_FG)
    svg.text(mx, 30,
             f"X = Milepost (WP mp 0 → HC mp {mp_max:.0f}, 1 MP = 12 layout in)  ·  "
             "Y = Railroad time  ·  Southward trains superior",
             size=9, fill=LBL_FG)
    svg.text(PAD_L - 4, plot_top - 5, "RR time", anchor="end", size=8, fill=LBL_FG)

    # ── NLS trains ─────────────────────────────────────────────────────────────
    for train in nls["trains"]:
        svc  = train["service"]
        dirn = train["direction"]
        num  = train["number"]
        clr  = SVC_CLR.get(svc, "#888888")
        if num == "11":
            clr = EXPRESS_CLR

        # Build stop list with pixel positions
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
            mp_exit = loc.get("milepost_exit")
            arr = t2m(entry.get("arrive"))
            dep = t2m(entry.get("depart"))
            ax  = stop_x(lid, mp, mp_exit, dirn, "arr")
            dx  = stop_x(lid, mp, mp_exit, dirn, "dep")
            stops.append({
                "lid": lid, "loc": loc, "mp": mp, "mp_exit": mp_exit,
                "arr": arr, "dep": dep, "ax": ax, "dx": dx,
                "note": entry.get("note", ""),
            })

        if not stops:
            continue

        prev_ax = None
        prev_t  = None

        for s in stops:
            lid     = s["lid"]
            arr, dep = s["arr"], s["dep"]
            ax, dx  = s["ax"], s["dx"]
            note    = s["note"]
            mp_exit = s["mp_exit"]

            t_arr = arr if arr is not None else dep
            t_dep = dep if dep is not None else arr

            # Travel diagonal from previous stop
            if prev_t is not None and prev_ax is not None and t_arr is not None:
                svg.line(prev_ax, Y(prev_t), ax, Y(t_arr), clr, W_TRAVEL)

            # Dwell
            if arr is not None and dep is not None and dep > arr:
                sw = W_BOLD if is_active(lid, note, svc) else W_THIN
                if mp_exit and abs(ax - dx) > 1:
                    # long siding or switchback with measurable dwell: diagonal
                    svg.line(ax, Y(arr), dx, Y(dep), clr, sw)
                else:
                    svg.line(ax, Y(arr), ax, Y(dep), clr, sw)

                # Mine spur dashed stub (setout/pickup notes)
                n = note.lower()
                if "setout" in n or "pickup" in n:
                    # start stub from the exit side facing the spur
                    spur_x0 = dx if dirn == "N" else ax
                    mid_t   = (arr + dep) / 2.0
                    for sl in nls["locations"]:
                        if (sl.get("within_limits_of") == lid
                                and sl.get("milepost") is not None):
                            svg.line(spur_x0, Y(mid_t), X(sl["milepost"]), Y(mid_t),
                                     clr, W_SPUR, dash=DASH_SP)
                            svg.text(X(sl["milepost"]) + 2, Y(mid_t) - 2,
                                     sl["id"], anchor="start", size=7, fill=clr)

            elif (arr is not None and dep is not None
                  and mp_exit and abs(ax - dx) > 1):
                # Switchback with arr==dep (zero-dwell run-around): thin connector
                svg.line(ax, Y(arr), dx, Y(dep), clr, W_THIN, dash="2,2")

            # Meet dot
            if meet_no(note):
                dot_y = Y(t_arr if t_arr is not None else t_dep)
                svg.circle(ax, dot_y, 3.5, MEET_CLR, stroke="white", sw=0.8)

            prev_ax = dx
            prev_t  = t_dep

        # Train number label — 1/3 along the first travel segment
        if len(stops) >= 2:
            s0, s1 = stops[0], stops[1]
            t0 = s0["dep"] if s0["dep"] is not None else s0["arr"]
            t1 = s1["arr"] if s1["arr"] is not None else s1["dep"]
            if t0 is not None and t1 is not None:
                frac = 1 / 3
                lx_ = s0["dx"] + (s1["ax"] - s0["dx"]) * frac
                ly_ = Y(t0 + (t1 - t0) * frac)
                xoff = 6 if dirn == "N" else -6
                anc  = "start" if dirn == "N" else "end"
                svg.text(lx_ + xoff, ly_ + 5, num,
                         anchor=anc, size=8, weight="bold", fill=clr)
        elif stops:
            s0  = stops[0]
            t0  = s0["dep"] if s0["dep"] is not None else s0["arr"]
            if t0 is not None:
                xoff = 6 if dirn == "N" else -6
                anc  = "start" if dirn == "N" else "end"
                svg.text(s0["dx"] + xoff, Y(t0) - 3, num,
                         anchor=anc, size=8, weight="bold", fill=clr)

    # ── C&O trains in dedicated strip ─────────────────────────────────────────
    coe_col = {"W": coe_w_x, "E": coe_e_x}

    for train in coe["trains"]:
        svc  = train["service"]
        dirn = train["direction"]
        num  = train["number"]
        clr  = COE_CLR.get(svc, "#888888")
        cx   = coe_col.get(dirn, coe_w_x)

        for entry in train["schedule"]:
            if entry["location"] != "WP_COE":
                continue
            arr  = t2m(entry.get("arrive"))
            dep  = t2m(entry.get("depart"))
            t_a  = arr if arr is not None else dep
            t_d  = dep if dep is not None else arr
            if t_a is None:
                continue

            y1  = Y(t_a)
            y2  = Y(t_d) if (t_d is not None and t_d > t_a) else y1 + 6
            sw_ = 3.5 if (t_d is not None and t_d > t_a) else 2.0
            svg.line(cx, y1, cx, y2, clr, sw_)

            lx_  = cx + (5 if dirn == "E" else -5)
            anc_ = "start" if dirn == "E" else "end"
            svg.text(lx_, y1 - 2, num, anchor=anc_, size=7,
                     weight="bold", fill=clr)

    # ── legend ────────────────────────────────────────────────────────────────
    lx = int(plot_left + plot_w) + 10
    ly = plot_top + 18

    svg.text(lx, ly - 8, "Legend", anchor="start", size=10,
             weight="bold", fill=TITLE_FG)

    for lbl, clr in [
        ("Passenger",       SVC_CLR["Pass"]),
        ("Freight",         SVC_CLR["Frght"]),
        ("Express Freight", EXPRESS_CLR),
        ("Coal / Coke",     SVC_CLR["Coal"]),
    ]:
        svg.line(lx, ly + 5, lx + 22, ly + 5, clr, W_TRAVEL + 0.5)
        svg.text(lx + 26, ly + 8, lbl, anchor="start", size=9, fill=LBL_FG)
        ly += 18

    ly += 6
    svg.text(lx, ly, "Dwell:", anchor="start", size=9, weight="bold", fill=TITLE_FG)
    ly += 14
    svg.line(lx, ly + 4, lx + 22, ly + 4, "#555555", W_BOLD)
    svg.text(lx + 26, ly + 7, "Active work", anchor="start", size=9, fill=LBL_FG)
    ly += 17
    svg.line(lx, ly + 4, lx + 22, ly + 4, "#555555", W_THIN)
    svg.text(lx + 26, ly + 7, "Schedule wait", anchor="start", size=9, fill=LBL_FG)
    ly += 17
    svg.line(lx, ly + 4, lx + 22, ly + 4, "#555555", W_THIN, dash="2,2")
    svg.text(lx + 26, ly + 7, "Switchback move", anchor="start", size=9, fill=LBL_FG)
    ly += 22

    svg.text(lx, ly, "Marks:", anchor="start", size=9, weight="bold", fill=TITLE_FG)
    ly += 14
    svg.line(lx, ly + 4, lx + 22, ly + 4, "#555555", W_SPUR, dash=DASH_SP)
    svg.text(lx + 26, ly + 7, "Mine spur work", anchor="start", size=9, fill=LBL_FG)
    ly += 17
    svg.circle(lx + 11, ly + 4, 3.5, MEET_CLR, stroke="white", sw=0.8)
    svg.text(lx + 26, ly + 7, "Meet point", anchor="start", size=9, fill=LBL_FG)
    ly += 22

    svg.text(lx, ly, "C&O strip:", anchor="start", size=9, weight="bold", fill=TITLE_FG)
    ly += 14
    svg.text(lx, ly + 8, "W col = westbound", anchor="start", size=8, fill=LBL_FG)
    ly += 14
    svg.text(lx, ly + 8, "E col = eastbound", anchor="start", size=8, fill=LBL_FG)
    ly += 20

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

    # ── write output ───────────────────────────────────────────────────────────
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(svg.render(total_w, total_h))
    print(f"Written: {OUTPUT}  ({total_w} × {total_h} px)")


if __name__ == "__main__":
    generate()
