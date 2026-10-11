import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PINK, BLUE, GREEN, INK = "#d6457a", "#2f7fb8", "#2f9a6a", "#1f1f24"
HUBS = {
    "patients": (PINK, "#fbd9e4"),
    "providers": (BLUE, "#d3e6f6"),
    "departments": (GREEN, "#d3eee0"),
}
TOP_ROW = ["notifications", "follow_up_tasks", "visit_summaries", "appointments", "referrals"]
BOTTOM_ROW = ["messages", "test_results", "medications", "prescriptions"]
CHAINS = {("appointments", "visit_summaries"), ("visit_summaries", "follow_up_tasks"), ("medications", "prescriptions")}
SHIFT = {"patients": -50, "departments": 50, "providers": 0}
W, HEAD, ROW, LEFT = 240, 38, 25, 40


def parse_schema():
    tables, links, current = {}, [], None
    for line in (ROOT / "schema.sql").read_text().splitlines():
        start = re.match(r"CREATE TABLE (\w+) \(", line)
        if start:
            current = start.group(1)
            tables[current] = []
        elif line.startswith(");"):
            current = None
        elif current:
            col = re.match(r"\s{2}(\w+)\s+(INTEGER|TEXT|REAL|BLOB)\b(.*)", line)
            if not col:
                continue
            rest = col.group(3)
            ref = re.search(r"REFERENCES (\w+)\(", rest)
            labels = [t for t, on in (("PK", "PRIMARY KEY" in rest), ("FK", ref), ("unique", "UNIQUE" in rest)) if on]
            tables[current].append((col.group(1), ", ".join(labels)))
            if ref:
                links.append((current, ref.group(1)))
    return tables, links


def height(columns):
    return HEAD + len(columns) * ROW + 12


def build():
    tables, links = parse_schema()
    placed = set(TOP_ROW + BOTTOM_ROW + list(HUBS) + ["quick_access_items"])
    assert placed == set(tables), f"layout is missing {set(tables) ^ placed}"
    h = {name: height(cols) for name, cols in tables.items()}

    top_y = 210
    green_y, pink_top = top_y + HEAD / 2 - 150, top_y - 52
    top_bottom = top_y + max(h[n] for n in TOP_ROW)
    blue_up = top_bottom + 54
    pink_low = blue_up + 48
    bottom_y = pink_low + 54
    bottom_bottom = bottom_y + max(h[n] for n in BOTTOM_ROW)
    blue_low = bottom_bottom + 54

    pos, row_x0, row_end = {}, LEFT + W + 56 + 40, 0
    for row, y in ((TOP_ROW, top_y), (BOTTOM_ROW, bottom_y)):
        x = row_x0
        for i, name in enumerate(row):
            pos[name] = (x, y)
            nxt = row[i + 1] if i + 1 < len(row) else None
            x += W + (64 if (name, nxt) in CHAINS or (nxt, name) in CHAINS else 30)
        row_end = max(row_end, x - 30)
    pink_trunk, blue_trunk = LEFT + W + 40, row_end + 40
    right_x = blue_trunk + 40
    pos["patients"] = (LEFT, (pink_top + pink_low) / 2 - h["patients"] / 2)
    pos["providers"] = (right_x, (blue_up + blue_low) / 2 - h["providers"] / 2)
    pos["departments"] = (right_x, green_y - HEAD / 2)
    pos["quick_access_items"] = (right_x, pos["providers"][1] + h["providers"] + 70)

    stubs = []
    for child, parent in links:
        if parent not in HUBS or child not in TOP_ROW + BOTTOM_ROW:
            continue
        top = child in TOP_ROW
        track = {"patients": pink_top if top else pink_low, "providers": blue_up if top else blue_low,
                 "departments": green_y}[parent]
        up = parent != "providers"
        shifted = top and child in ("appointments", "referrals")
        x = pos[child][0] + W / 2 + (SHIFT[parent] if shifted else 0)
        edge = pos[child][1] if up else pos[child][1] + h[child]
        stubs.append({"hub": parent, "x": x, "edge": edge, "track": track})

    verticals, horizontals = [], []
    for s in stubs:
        verticals.append((s["x"], min(s["edge"], s["track"]), max(s["edge"], s["track"]), HUBS[s["hub"]][0]))
    for hub, trunk_x, edge_x in (("patients", pink_trunk, LEFT + W), ("providers", blue_trunk, right_x)):
        tracks = sorted({s["track"] for s in stubs if s["hub"] == hub})
        for ty in tracks:
            xs = [s["x"] for s in stubs if s["hub"] == hub and s["track"] == ty]
            horizontals.append((ty, trunk_x, max(xs) if trunk_x < min(xs) else min(xs), HUBS[hub][0]))
        mid = pos[hub][1] + h[hub] / 2
        horizontals.append((mid, trunk_x, edge_x, HUBS[hub][0]))
        verticals.append((trunk_x, min(tracks + [mid]), max(tracks + [mid]), HUBS[hub][0]))
    horizontals.append((green_y, right_x, min(s["x"] for s in stubs if s["hub"] == "departments"), GREEN))

    plain = []
    for child, parent in links:
        if parent in HUBS and child in TOP_ROW + BOTTOM_ROW:
            continue
        if parent == "departments":
            x = right_x + W / 2
            plain.append((GREEN, f"M{x:.1f} {pos[parent][1] + h[parent]:.1f} V{pos[child][1]:.1f}"))
            continue
        (px, py), (qx, _) = pos[parent], pos[child]
        y = py + HEAD / 2
        a, b = (px, qx + W) if px > qx else (px + W, qx)
        plain.append(("#555555", f"M{a:.1f} {y:.1f} H{b:.1f}"))

    def hopped(y, x1, x2, color):
        step = 1 if x2 > x1 else -1
        lo, hi = sorted((x1, x2))
        path = f"M{x1:.1f} {y:.1f}"
        crossings = [vx for vx, y1, y2, vc in verticals if vc != color and lo < vx < hi and y1 < y < y2]
        for vx in sorted(crossings, reverse=step < 0):
            path += f" H{vx - 6 * step:.1f} a6 6 0 0 {1 if step > 0 else 0} {12 * step} 0"
        return path + f" H{x2:.1f}"

    lines = "".join(f'<path d="{d}" stroke="{c}" stroke-width="2.4" fill="none"/>' for c, d in plain)
    lines += "".join(f'<path d="M{x:.1f} {a:.1f} V{b:.1f}" stroke="{c}" stroke-width="2.4" fill="none"/>' for x, a, b, c in verticals)
    lines += "".join(f'<path d="{hopped(y, a, b, c)}" stroke="{c}" stroke-width="2.4" fill="none"/>' for y, a, b, c in horizontals)

    boxes = []
    for name, (x, y) in pos.items():
        fill = HUBS.get(name, (None, "#eceef2"))[1]
        dash = ' stroke-dasharray="6 5"' if name == "quick_access_items" else ""
        boxes.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{W}" height="{h[name]}" rx="4" fill="#ffffff" stroke="{INK}" stroke-width="1.5"{dash}/>')
        boxes.append(f'<path d="M{x:.1f} {y + 4:.1f} a4 4 0 0 1 4 -4 H{x + W - 4:.1f} a4 4 0 0 1 4 4 V{y + HEAD:.1f} H{x:.1f} Z" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>')
        boxes.append(f'<text x="{x + 12:.1f}" y="{y + 25:.1f}" font-size="18" font-weight="700" fill="{INK}">{name}</text>')
        for i, (col, label) in enumerate(tables[name]):
            ty = y + HEAD + i * ROW + 19
            shown = f"{col} ({label})" if label else col
            weight = ' font-weight="700"' if "PK" in label else ""
            boxes.append(f'<text x="{x + 12:.1f}" y="{ty:.1f}" font-size="15"{weight} fill="{INK}">{shown}</text>')

    width = right_x + W + 40
    bottom = max(blue_low + 40, pos["quick_access_items"][1] + h["quick_access_items"] + 40)
    total = max(round(width * 9 / 16), round(bottom))
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {total}" width="{width:.0f}" height="{total}" '
        f'font-family="Arial, Helvetica, sans-serif">'
        f'<rect width="100%" height="100%" fill="#ffffff"/>'
        f'<text x="{LEFT}" y="62" font-size="32" font-weight="700" fill="{INK}">Care Overview database</text>'
        f'{lines}{"".join(boxes)}</svg>'
    ), width, total


if __name__ == "__main__":
    svg, width, total = build()
    out = ROOT / "docs"
    (out / "er_diagram.svg").write_text(svg)
    if "--png" in sys.argv:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                        f"--window-size={width:.0f},{total}", f"--screenshot={out / 'er_diagram.png'}",
                        f"file://{out / 'er_diagram.svg'}"], capture_output=True)
    print("wrote", out / "er_diagram.svg", file=sys.stderr)
