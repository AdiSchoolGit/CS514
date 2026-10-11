import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PINK, BLUE, GREEN = "#d6457a", "#2f7fb8", "#2f9a6a"
INK, MUTED, LINE = "#2b2b33", "#7b7b88", "#8a8a96"
HUBS = {
    "patients": (PINK, "#ffe3ec"),
    "providers": (BLUE, "#dcecf8"),
    "departments": (GREEN, "#dcf3e8"),
}
TOP_ROW = ["notifications", "follow_up_tasks", "visit_summaries", "appointments", "referrals"]
BOTTOM_ROW = ["messages", "test_results", "medications", "prescriptions"]
CHAINS = {("appointments", "visit_summaries"), ("visit_summaries", "follow_up_tasks"), ("medications", "prescriptions")}
HUB_PORTS = {
    ("top", "patients"): "top", ("top", "departments"): "top", ("top", "providers"): "bottom",
    ("bottom", "patients"): "top", ("bottom", "providers"): "bottom",
}
STUB_SHIFT = {"patients": -1, "departments": 1, "providers": 0}


def parse_schema():
    tables = {}
    current = None
    for line in (ROOT / "schema.sql").read_text().splitlines():
        start = re.match(r"CREATE TABLE (\w+) \(", line)
        if start:
            current = tables.setdefault(start.group(1), [])
            continue
        if line.startswith(");"):
            current = None
            continue
        col = re.match(r"\s{2}(\w+)\s+(INTEGER|TEXT|REAL|BLOB)\b(.*)", line)
        if current is not None and col:
            rest = col.group(3)
            ref = re.search(r"REFERENCES (\w+)\(", rest)
            current.append({
                "name": col.group(1),
                "type": "int" if col.group(2) == "INTEGER" else col.group(2).lower(),
                "pk": "PRIMARY KEY" in rest,
                "fk": ref.group(1) if ref else None,
                "uk": "UNIQUE" in rest,
                "null": "NOT NULL" not in rest and "PRIMARY KEY" not in rest,
            })
    return tables


class Style:
    def __init__(self, full):
        self.full = full
        self.s = 1.0 if full else 1.25
        self.row_h = round(22 * self.s)
        self.head = round(30 * self.s)
        self.font = 12.5 * self.s
        self.head_font = 14 * self.s
        self.small = 10 * self.s
        self.box_w = 250 if full else 222
        self.hub_w = 214
        self.tag_w = round(52 * self.s)


class Box:
    def __init__(self, name, cols, style, x, w):
        self.name, self.cols, self.style, self.x, self.w = name, cols, style, x, w
        if style.full:
            self.rows, self.hidden = cols, 0
        else:
            self.rows = [c for c in cols if c["pk"] or c["fk"] or c["uk"]]
            self.hidden = len(cols) - len(self.rows)
        extra = 0
        self.h = style.head + (len(self.rows) + extra) * style.row_h + 8
        self.y = 0

    def row_y(self, col_name):
        index = next(i for i, c in enumerate(self.rows) if c["name"] == col_name)
        return self.y + self.style.head + index * self.style.row_h + self.style.row_h / 2

    @property
    def right(self):
        return self.x + self.w

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def bottom(self):
        return self.y + self.h


def symbol(x, y, dx, dy, kind, color=LINE):
    nx, ny = -dy, dx

    def at(t, s=0):
        return x + dx * t + nx * s, y + dy * t + ny * s

    def seg(a, b):
        return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>'

    parts = []
    if kind == "one":
        parts += [seg(at(8, 6), at(8, -6)), seg(at(14, 6), at(14, -6))]
    elif kind == "zero_one":
        cx, cy = at(19)
        parts += [seg(at(8, 6), at(8, -6)), f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="#fff"/>']
    elif kind == "zero_many":
        cx, cy = at(19)
        parts += [seg(at(12), at(0, 6)), seg(at(12), at(0)), seg(at(12), at(0, -6)),
                  f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="#fff"/>']
    return f'<g stroke="{color}" stroke-width="1.6" fill="none">{"".join(parts)}</g>'


def classify(tables):
    hub_links, chain_links = [], []
    for child, cols in tables.items():
        for col in cols:
            parent = col["fk"]
            if not parent:
                continue
            parent_kind = "zero_one" if col["null"] else "one"
            child_kind = "zero_one" if col["uk"] else "zero_many"
            if parent in HUBS and child in TOP_ROW + BOTTOM_ROW:
                hub_links.append((child, parent, child_kind))
            elif (parent, child) in CHAINS:
                chain_links.append((parent, child, parent_kind, child_kind))
            elif (parent, child) == ("departments", "providers"):
                chain_links.append((parent, child, parent_kind, child_kind))
            else:
                raise SystemExit(f"no layout for {child}.{col['name']} -> {parent}")
    return hub_links, chain_links


def build(full):
    st = Style(full)
    tables = parse_schema()
    hub_links, chain_links = classify(tables)

    boxes = {}
    for name in TOP_ROW + BOTTOM_ROW:
        boxes[name] = Box(name, tables[name], st, 0, st.box_w)
    for name in HUBS:
        boxes[name] = Box(name, tables[name], st, 0, st.hub_w)
    boxes["quick_access_items"] = Box("quick_access_items", tables["quick_access_items"], st, 0, st.hub_w)

    left, linked_gap, gap = 40, 64, 30
    pink_trunk = left + st.hub_w + 40
    row_x0 = pink_trunk + 36

    def place_row(names, y):
        x = row_x0
        for i, name in enumerate(names):
            boxes[name].x, boxes[name].y = x, y
            nxt = names[i + 1] if i + 1 < len(names) else None
            linked = (name, nxt) in CHAINS or (nxt, name) in CHAINS
            x += st.box_w + (linked_gap if linked else gap)
        return x - gap

    top_y = 215 if not full else 215
    row_end = place_row(TOP_ROW, top_y)
    top_bottom = max(boxes[n].bottom for n in TOP_ROW)
    track = {
        ("green", "top"): top_y - 100,
        ("pink", "top"): top_y - 56,
        ("blue", "upper"): top_bottom + 40,
        ("pink", "lower"): top_bottom + 78,
    }
    bottom_y = track[("pink", "lower")] + 40
    place_row(BOTTOM_ROW, bottom_y)
    bottom_bottom = max(boxes[n].bottom for n in BOTTOM_ROW)
    track[("blue", "lower")] = bottom_bottom + 46

    blue_trunk = row_end + 40
    hub_right_x = blue_trunk + 40
    for name in ("providers", "departments", "quick_access_items"):
        boxes[name].x = hub_right_x
    boxes["patients"].x = left

    pink_span = (track[("pink", "top")], track[("pink", "lower")])
    blue_span = (track[("blue", "upper")], track[("blue", "lower")])
    boxes["patients"].y = (pink_span[0] + pink_span[1]) / 2 - boxes["patients"].h / 2
    boxes["providers"].y = (blue_span[0] + blue_span[1]) / 2 - boxes["providers"].h / 2
    green_y = track[("green", "top")]
    boxes["departments"].y = green_y - st.head - st.row_h / 2

    stubs = []
    for child, hub, child_kind in hub_links:
        row = "top" if child in TOP_ROW else "bottom"
        port = HUB_PORTS[(row, hub)]
        color = HUBS[hub][0]
        if hub == "patients":
            ty = track[("pink", "top" if row == "top" else "lower")]
        elif hub == "providers":
            ty = track[("blue", "upper" if row == "top" else "lower")]
        else:
            ty = track[("green", "top")]
        box = boxes[child]
        shifted = row == "top" and child in ("appointments", "referrals")
        sx = box.cx + (STUB_SHIFT[hub] * 42 if shifted else 0)
        edge_y = box.y if port == "top" else box.bottom
        stubs.append({"hub": hub, "color": color, "x": sx, "y1": edge_y, "y2": ty, "port": port, "kind": child_kind})

    verticals, horizontals, dots, symbols, joins = [], [], [], [], []
    for stub in stubs:
        verticals.append((stub["x"], min(stub["y1"], stub["y2"]), max(stub["y1"], stub["y2"]), stub["color"]))
        dots.append((stub["x"], stub["y2"], stub["color"]))
        symbols.append(symbol(stub["x"], stub["y1"], 0, -1 if stub["port"] == "top" else 1, stub["kind"], stub["color"]))

    patients, providers, dept = boxes["patients"], boxes["providers"], boxes["departments"]
    for hub, hub_box, trunk_x, edge_x, direction in (
        ("patients", patients, pink_trunk, patients.right, 1),
        ("providers", providers, blue_trunk, providers.x, -1),
    ):
        color = HUBS[hub][0]
        track_ys = sorted({st["y2"] for st in stubs if st["hub"] == hub})
        for ty in track_ys:
            xs = [st["x"] for st in stubs if st["hub"] == hub and st["y2"] == ty]
            horizontals.append((ty, trunk_x, max(xs) if trunk_x < min(xs) else min(xs), color))
            joins.append((trunk_x, ty, color))
        stub_y = hub_box.row_y("id")
        horizontals.append((stub_y, trunk_x, edge_x, color))
        symbols.append(symbol(edge_x, stub_y, direction, 0, "one", color))
        joins.append((trunk_x, stub_y, color))
        verticals.append((trunk_x, min(track_ys + [stub_y]), max(track_ys + [stub_y]), color))

    dept_y = dept.row_y("id")
    dept_xs = [st["x"] for st in stubs if st["hub"] == "departments"]
    horizontals.append((dept_y, dept.x, min(dept_xs), GREEN))
    symbols.append(symbol(dept.x, dept_y, -1, 0, "one", GREEN))

    connectors = []
    for parent, child, parent_kind, child_kind in chain_links:
        p, c = boxes[parent], boxes[child]
        if parent == "departments":
            x = p.cx
            connectors.append((GREEN, f"M{x:.1f} {p.bottom:.1f} V{c.y:.1f}"))
            symbols.append(symbol(x, p.bottom, 0, 1, parent_kind, GREEN))
            symbols.append(symbol(x, c.y, 0, -1, child_kind, GREEN))
            continue
        y = p.y + st.head + st.row_h / 2
        if p.x < c.x:
            a, b, da, db = p.right, c.x, 1, -1
        else:
            a, b, da, db = p.x, c.right, -1, 1
        connectors.append((LINE, f"M{a:.1f} {y:.1f} H{b:.1f}"))
        symbols.append(symbol(a, y, da, 0, parent_kind))
        symbols.append(symbol(b, y, db, 0, child_kind))

    def hopped(y, x1, x2, color):
        step = 1 if x2 > x1 else -1
        lo, hi = sorted((x1, x2))
        path = f"M{x1:.1f} {y:.1f}"
        hops = sorted((vx for vx, y1, y2, vc in verticals if vc != color and lo < vx < hi and y1 < y < y2), reverse=step < 0)
        for vx in hops:
            path += f" H{vx - 5 * step:.1f} a5 5 0 0 {1 if step > 0 else 0} {10 * step} 0"
        return path + f" H{x2:.1f}"

    paths = "".join(f'<path d="{d}" stroke="{c}" stroke-width="2" fill="none"/>' for c, d in connectors)
    paths += "".join(f'<path d="M{x:.1f} {y1:.1f} V{y2:.1f}" stroke="{c}" stroke-width="2" fill="none"/>' for x, y1, y2, c in verticals)
    paths += "".join(f'<path d="{hopped(y, a, b, c)}" stroke="{c}" stroke-width="2" fill="none"/>' for y, a, b, c in horizontals)
    paths += "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{c}"/>' for x, y, c in dots + joins)

    strip_y = max(bottom_bottom + 120, boxes["providers"].bottom + 60)
    boxes["quick_access_items"].y = strip_y - 14

    body = []
    for name, box in boxes.items():
        color, fill = HUBS.get(name, (LINE, "#eef0f3"))
        dash = ' stroke-dasharray="6 5"' if name == "quick_access_items" else ""
        body.append(f'<rect x="{box.x:.1f}" y="{box.y:.1f}" width="{box.w}" height="{box.h}" rx="9" fill="#fff" stroke="{color}" stroke-width="1.8"{dash}/>')
        body.append(f'<path d="M{box.x:.1f} {box.y + 9:.1f} a9 9 0 0 1 9 -9 H{box.right - 9:.1f} a9 9 0 0 1 9 9 V{box.y + st.head:.1f} H{box.x:.1f} Z" fill="{fill}"/>')
        body.append(f'<text x="{box.x + 14:.1f}" y="{box.y + st.head * 0.68:.1f}" font-size="{st.head_font:.1f}" font-weight="700" fill="{INK}">{name}</text>')
        for i, col in enumerate(box.rows):
            ry = box.y + st.head + i * st.row_h + st.row_h / 2
            tags = [t for t, on in (("PK", col["pk"]), ("FK", col["fk"]), ("UK", col["uk"])) if on]
            if tags:
                badge = {"PK": "#fff1c9", "FK": "#ffe3ec", "UK": "#ece6ff"}[tags[0]]
                w = (14 + 12 * len(tags) + 5 * (len(tags) - 1)) * st.s * 0.9 + 6
                body.append(f'<rect x="{box.x + 10:.1f}" y="{ry - 9 * st.s * 0.9:.1f}" width="{w:.1f}" height="{18 * st.s * 0.9:.1f}" rx="4" fill="{badge}"/>')
                body.append(f'<text x="{box.x + 10 + w / 2:.1f}" y="{ry + 3.6 * st.s:.1f}" font-size="{st.small:.1f}" font-weight="700" text-anchor="middle" fill="{INK}">{" ".join(tags)}</text>')
            body.append(f'<text x="{box.x + 10 + st.tag_w + 8:.1f}" y="{ry + 4.5 * st.s:.1f}" font-size="{st.font:.1f}" fill="{INK}">{col["name"]}</text>')

    legend = [f'<text x="{left}" y="{strip_y}" font-size="{st.font * 0.95:.1f}" font-weight="700" fill="{INK}">How to read this</text>']
    for i, (kind, label) in enumerate((("one", "exactly one"), ("zero_one", "zero or one"), ("zero_many", "zero or many"))):
        lx = left + i * 250
        ly = strip_y + 34
        legend.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 56}" y2="{ly}" stroke="{LINE}" stroke-width="1.6"/>')
        legend.append(symbol(lx, ly, 1, 0, kind))
        legend.append(f'<text x="{lx + 68}" y="{ly + 5}" font-size="{st.font * 0.9:.1f}" fill="{INK}">{label}</text>')
    for i, (color, label) in enumerate(((PINK, "belongs to a patient"), (BLUE, "involves a provider"), (GREEN, "involves a department"))):
        lx = left + i * 250
        ly = strip_y + 70
        legend.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 56}" y2="{ly}" stroke="{color}" stroke-width="2.4"/>')
        legend.append(f'<text x="{lx + 68}" y="{ly + 5}" font-size="{st.font * 0.9:.1f}" fill="{INK}">{label}</text>')
    quick = boxes.pop("quick_access_items")

    width = hub_right_x + st.hub_w + 40
    height = max(strip_y + 120, quick.bottom + 50)
    shift = 0
    if not full and height < width * 9 / 16:
        shift = (width * 9 / 16 - height) * 0.45
        height = width * 9 / 16
    title_size = 30 if not full else 24
    header = (
        f'<text x="{left}" y="52" font-size="{title_size}" font-weight="800" fill="{INK}">Care Overview database</text>'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" width="{width:.0f}" height="{height:.0f}" '
        f'font-family="-apple-system, \'Segoe UI\', Helvetica, Arial, sans-serif">'
        f'<rect width="100%" height="100%" fill="#ffffff"/>' + header
        + f'<g transform="translate(0 {shift:.1f})">'
        + paths + "".join(body) + "".join(symbols) + "".join(legend) + "</g></svg>"
    )


if __name__ == "__main__":
    out = ROOT / "docs"
    (out / "er_diagram.svg").write_text(build(False))
    (out / "er_diagram_full.svg").write_text(build(True))
    print("wrote", out / "er_diagram.svg", "and", out / "er_diagram_full.svg", file=sys.stderr)
