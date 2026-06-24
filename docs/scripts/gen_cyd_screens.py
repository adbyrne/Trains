#!/usr/bin/env python3
"""
Generate simulated CYD touchscreen renders for the DO article.
Scenario: No. 52 South meets Extra 14 North at Jacks Creek (Form 31 / Form A).
Station: JC at 7:09 AM fast-clock time.

Output: docs/diagrams/cyd_screens/cyd_screen_{clock,os_entry,orders,next_station}.png
Run from any directory: python3 docs/scripts/gen_cyd_screens.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(SCRIPT_DIR, "../diagrams/cyd_screens")

W, H = 640, 480

# --- Palette (matching Station_OS firmware colors) ---
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
YELLOW      = (255, 215, 0)
GREEN       = (64, 220, 64)
CYAN        = (64, 220, 220)
GRAY        = (136, 136, 136)
MED_GRAY    = (68, 68, 68)
DARK_GREEN  = (27, 94, 32)     # ACK button / selected direction key

# --- Scenario data ---
STATION_ID   = "JC"
FAST_TIME    = "7:09 AM"
NB_TRAIN     = "No.1"
NB_TIME      = "7:46 AM"
SB_TRAIN     = "No.52"
SB_TIME      = "7:09 AM"
ENTERED_TRAIN = "No. 52"
DIRECTION    = "S"
FORM_DELIVERY = "31"
ORDER_NUM    = "1"
ORDER_TEXT   = "No. 52 will meet Extra 14 North at Jacks Creek."
NEXT_DIR     = "SOUTHBOUND"
NEXT_STATION = "Becs Bend"
OPP_TRAIN    = "No.1"
OPP_TIME     = "Ar  7:31 AM"

FONT_DIR = "/usr/share/fonts/liberation-sans"

def f(name, size):
    path = os.path.join(FONT_DIR, f"{name}.ttf")
    return ImageFont.truetype(path, size)

BOLD = "LiberationSans-Bold"
REG  = "LiberationSans-Regular"

def center_x(d, text, font, y, color):
    bbox = d.textbbox((0, 0), text, font=font)
    x = (W - (bbox[2] - bbox[0])) // 2
    d.text((x, y), text, fill=color, font=font)

def wrap_text(d, text, font, max_w):
    """Return list of lines that fit within max_w pixels."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = d.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_w and current:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    return lines


# ── Screen 1: Clock ─────────────────────────────────────────────────────────

def make_clock():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)

    d.text((18, 14), STATION_ID, fill=YELLOW, font=f(BOLD, 38))
    d.ellipse((W - 42, 16, W - 18, 40), fill=GREEN)

    time_font = f(BOLD, 100)
    bbox = d.textbbox((0, 0), FAST_TIME, font=time_font)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) // 2, 110), FAST_TIME, fill=WHITE, font=time_font)

    d.line([(18, 310), (W - 18, 310)], fill=GRAY, width=1)

    info_font = f(BOLD, 30)
    d.text((30, 335), f"NB: {NB_TRAIN}   {NB_TIME}", fill=GREEN, font=info_font)
    d.text((30, 385), f"SB: {SB_TRAIN}   {SB_TIME}", fill=CYAN, font=info_font)

    out = os.path.join(OUT_DIR, "cyd_screen_clock.png")
    img.save(out)
    print(f"  clock → {out}")


# ── Screen 2: OS Entry ───────────────────────────────────────────────────────

def make_os_entry():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)

    d.text((18, 14), ENTERED_TRAIN, fill=WHITE, font=f(BOLD, 38))
    d.text((W - 90, 14), f"[{DIRECTION}]", fill=GREEN, font=f(BOLD, 38))

    keys = [
        ["1", "2", "3", "N"],
        ["4", "5", "6", "S"],
        ["7", "8", "9", "X"],
        ["⌫", "0", "✓", "WX"],
    ]

    key_w, key_h = 140, 88
    gap = 10
    start_x, start_y = 20, 80
    key_font = f(BOLD, 36)

    for ri, row in enumerate(keys):
        for ci, key in enumerate(row):
            kx = start_x + ci * (key_w + gap)
            ky = start_y + ri * (key_h + gap)

            if key == DIRECTION:
                bg, fg = DARK_GREEN, GREEN
            elif key == "✓":
                bg, fg = DARK_GREEN, GREEN
            else:
                bg, fg = MED_GRAY, WHITE

            d.rounded_rectangle([kx, ky, kx + key_w, ky + key_h], radius=8, fill=bg)

            bbox = d.textbbox((0, 0), key, font=key_font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            d.text((kx + (key_w - tw) // 2, ky + (key_h - th) // 2 - 4),
                   key, fill=fg, font=key_font)

    out = os.path.join(OUT_DIR, "cyd_screen_os_entry.png")
    img.save(out)
    print(f"  os_entry → {out}")


# ── Screen 3: Orders ─────────────────────────────────────────────────────────

def make_orders():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)

    d.text((18, 14), f"Form {FORM_DELIVERY}   #{ORDER_NUM}", fill=GRAY, font=f(REG, 24))

    order_font = f(BOLD, 36)
    lines = wrap_text(d, ORDER_TEXT, order_font, W - 40)
    y = 80
    for line in lines:
        d.text((18, y), line, fill=YELLOW, font=order_font)
        y += 54

    btn_h = 70
    btn_y = H - btn_h - 20
    d.rounded_rectangle([20, btn_y, W - 20, btn_y + btn_h], radius=12, fill=DARK_GREEN)
    ack_font = f(BOLD, 30)
    ack_text = "ACK — Order Received"
    bbox = d.textbbox((0, 0), ack_text, font=ack_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text(((W - tw) // 2, btn_y + (btn_h - th) // 2 - 2),
           ack_text, fill=WHITE, font=ack_font)

    out = os.path.join(OUT_DIR, "cyd_screen_orders.png")
    img.save(out)
    print(f"  orders → {out}")


# ── Screen 4: Next Station ───────────────────────────────────────────────────

def make_next_station():
    img = Image.new("RGB", (W, H), BLACK)
    d = ImageDraw.Draw(img)

    center_x(d, NEXT_DIR, f(BOLD, 40), 30, GREEN)

    stn_font = f(BOLD, 54)
    bbox = d.textbbox((0, 0), NEXT_STATION, font=stn_font)
    center_x(d, NEXT_STATION, stn_font, 160, WHITE)

    train_text = f"{OPP_TRAIN}    {OPP_TIME}"
    center_x(d, train_text, f(BOLD, 34), 290, CYAN)

    footer = "touch to return to clock"
    center_x(d, footer, f(REG, 20), H - 40, GRAY)

    out = os.path.join(OUT_DIR, "cyd_screen_next_station.png")
    img.save(out)
    print(f"  next_station → {out}")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    print("Generating CYD screen renders...")
    make_clock()
    make_os_entry()
    make_orders()
    make_next_station()
    print("Done.")
