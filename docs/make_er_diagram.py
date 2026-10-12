import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def parse_schema():
    tables = {}
    current = None
    for line in (ROOT / "schema.sql").read_text().splitlines():
        match = re.match(r"CREATE TABLE (\w+) \(", line)
        if match:
            current = tables.setdefault(match.group(1), [])
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
            })
    return tables


def make_svg(tables, show_all_cols=False):
    box_w = 220
    col_h = 22
    header_h = 30
    gap = 30
    cols_per_row = 4

    boxes = []
    x, y = 40, 60
    col_num = 0
    row_max_h = 0

    for name, cols in tables.items():
        if show_all_cols:
            visible = cols
        else:
            visible = [c for c in cols if c["pk"] or c["fk"]]

        box_h = header_h + len(visible) * col_h + 8
        row_max_h = max(row_max_h, box_h)

        box = f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="8" fill="#fff" stroke="#888" stroke-width="1.5"/>'
        box += f'<rect x="{x}" y="{y}" width="{box_w}" height="{header_h}" rx="8" fill="#e8e8e8"/>'
        box += f'<rect x="{x}" y="{y+8}" width="{box_w}" height="{header_h-8}" fill="#e8e8e8"/>'
        box += f'<text x="{x+12}" y="{y+20}" font-size="13" font-weight="bold">{name}</text>'

        for i, col in enumerate(visible):
            cy = y + header_h + i * col_h + 16
            label = col["name"]
            if col["pk"]:
                box += f'<rect x="{x+8}" y="{cy-11}" width="22" height="16" rx="3" fill="#fff1c9"/>'
                box += f'<text x="{x+19}" y="{cy+2}" font-size="9" font-weight="bold" text-anchor="middle">PK</text>'
            if col["fk"]:
                fx = x + 34 if col["pk"] else x + 8
                box += f'<rect x="{fx}" y="{cy-11}" width="20" height="16" rx="3" fill="#ffe3ec"/>'
                box += f'<text x="{fx+10}" y="{cy+2}" font-size="9" font-weight="bold" text-anchor="middle">FK</text>'
            tx = x + 60
            box += f'<text x="{tx}" y="{cy+2}" font-size="12">{label}</text>'

        boxes.append(box)
        col_num += 1
        x += box_w + gap

        if col_num >= cols_per_row:
            col_num = 0
            x = 40
            y += row_max_h + gap
            row_max_h = 0

    width = 40 + cols_per_row * (box_w + gap)
    height = y + row_max_h + 40

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" font-family="sans-serif">'
    svg += '<rect width="100%" height="100%" fill="#fff"/>'
    svg += f'<text x="40" y="40" font-size="20" font-weight="bold">Care Overview Database</text>'
    svg += "".join(boxes)
    svg += '</svg>'
    return svg


if __name__ == "__main__":
    tables = parse_schema()
    out = ROOT / "docs"
    (out / "er_diagram.svg").write_text(make_svg(tables, False))
    (out / "er_diagram_full.svg").write_text(make_svg(tables, True))
    print(f"Generated ER diagrams in {out}")
