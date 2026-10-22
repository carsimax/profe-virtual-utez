"""Gráficas SVG temáticas para el deck (usan las clases .ch-* y --series-N del diseño UTEZ).
Uso: python3 svg_charts.py datos.json > grafica.svg     (o --demo para ver un ejemplo)
spec: {"type": "bar" | "hbar" | "line", "title": "texto para aria-label",
       "categories": ["Ene", "Feb"], "series": [{"name": "2026", "values": [1, 2]}],
       "unit": "%" (texto como " min" lleva espacio duro automático),
       "focus": "Feb" (opcional, solo con 1 serie: resalta una categoría; el resto en gris),
       "label": "end" | "max" | "all" (opcional), "width": 1000, "height": 560}"""
import json, math, sys
from html import escape

def fmt(v, unit=""):
    if unit and unit[0].isalpha(): unit = "\u00a0" + unit
    elif unit.startswith(" "): unit = "\u00a0" + unit.lstrip()
    a = abs(v)
    s = (f"{v/1e6:.1f}M" if a >= 1e6 else f"{v/1e3:.1f}K" if a >= 1e4 else
         f"{v:,.0f}" if a >= 100 or float(v).is_integer() else f"{v:.1f}")
    return s.replace(".0M", "M").replace(".0K", "K") + unit

def scale(vmax_data):
    """Devuelve (máximo del eje, paso) con pasos redondos: 1, 2, 2.5, 3, 4, 5 × 10^k."""
    raw = max(vmax_data * 1.08, 1e-9)
    e = 10 ** math.floor(math.log10(raw / 4)); f = raw / 4 / e
    step = next(n for n in (1, 2, 2.5, 3, 4, 5, 10) if f <= n) * e
    return step * math.ceil(raw / step), step

def bar_path(x, y, w, h, r, horizontal=False):
    """Barra con extremo de datos redondeado y base recta."""
    r = min(r, w / 2, h / 2) if h > 0 and w > 0 else 0
    if horizontal:  # base a la izquierda, extremo a la derecha
        return f"M{x},{y}H{x+w-r}Q{x+w},{y} {x+w},{y+r}V{y+h-r}Q{x+w},{y+h} {x+w-r},{y+h}H{x}Z"
    return f"M{x},{y+h}V{y+r}Q{x},{y} {x+r},{y}H{x+w-r}Q{x+w},{y} {x+w},{y+r}V{y+h}Z"

def wrap(text, maxch):
    """Split a label into at most 3 lines of about maxch characters."""
    out, cur = [], ""
    for w in str(text).split():
        if cur and len(cur) + 1 + len(w) > maxch: out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    out.append(cur)
    return out[:3]

def legend(series, x, y):
    out, cx = [], x
    for i, s in enumerate(series):
        out.append(f'<rect class="ch-s{i+1}" x="{cx}" y="{y-14}" width="18" height="18" rx="4"/>'
                   f'<text class="ch-label" x="{cx+28}" y="{y+1}">{escape(s["name"])}</text>')
        cx += 28 + 14 * len(s["name"]) + 40
    return "".join(out)

def chart(spec):
    t, cats, series = spec.get("type", "bar"), spec["categories"], spec["series"][:4]
    W, H, unit = spec.get("width", 900), spec.get("height", 520), spec.get("unit", "")
    multi = len(series) > 1
    focus, mode = (None if multi else spec.get("focus")), spec.get("label", "end" if t == "line" else "all")
    if mode is True: mode = "all"
    if t == "bar" and max(len(c) for c in cats) * 11 > (W - 96) / len(cats) * 2.6: t = "hbar"   # long labels: horizontal bars
    top = 64 if multi else 24
    vmax, step = scale(max(max(s["values"]) for s in series))
    ticks = [step * k for k in range(round(vmax / step) + 1)]
    parts, desc = [], "; ".join(f'{s["name"]}: ' + ", ".join(f"{c} {fmt(v, unit)}" for c, v in zip(cats, s["values"])) for s in series)
    if multi: parts.append(legend(series, 0, 28))
    if t == "hbar":
        L, R, B = max(len(c) for c in cats) * 13 + 24, 90, 44
        pw, ph = W - L - R, H - top - B
        band = ph / len(cats); bh = min(56, band * 0.6 / len(series))
        for tv in ticks:
            gx = L + pw * tv / vmax
            parts.append(f'<line class="ch-grid" x1="{gx:.1f}" y1="{top}" x2="{gx:.1f}" y2="{H-B}"/>'
                         f'<text class="ch-tick" x="{gx:.1f}" y="{H-B+32}" text-anchor="middle">{fmt(tv)}</text>')
        for ci, c in enumerate(cats):
            y0 = top + band * ci + (band - bh * len(series) - 3 * (len(series) - 1)) / 2
            parts.append(f'<text class="ch-label" x="{L-16}" y="{top+band*ci+band/2+8:.1f}" text-anchor="end">{escape(c)}</text>')
            for si, s in enumerate(series):
                v = s["values"][ci]; w = pw * v / vmax; y = y0 + si * (bh + 3)
                cls = f"ch-s{si+1}" + (" ch-mute" if focus is not None and c != focus else "")
                parts.append(f'<path class="{cls}" d="{bar_path(L, y, w, bh, 6, True)}"><title>{escape(c)} · {escape(s["name"])}: {fmt(v, unit)}</title></path>')
                if mode == "all" or (mode == "max" and v == max(s["values"])) or c == focus:
                    parts.append(f'<text class="ch-value" x="{L+w+12:.1f}" y="{y+bh/2+8:.1f}">{fmt(v, unit)}</text>')
        parts.append(f'<line class="ch-axis" x1="{L}" y1="{top}" x2="{L}" y2="{H-B}"/>')
    else:
        maxch = max(4, int((W - 96) / len(cats) / 11))
        nl = max(len(wrap(c, maxch)) for c in cats) if t == "bar" else 1
        L, R, B = 72, 120 if t == "line" else 24, 52 + 26 * (nl - 1)
        pw, ph = W - L - R, H - top - B
        for tv in ticks:
            gy = top + ph - ph * tv / vmax
            parts.append(f'<line class="ch-grid" x1="{L}" y1="{gy:.1f}" x2="{L+pw}" y2="{gy:.1f}"/>'
                         f'<text class="ch-tick" x="{L-14}" y="{gy+6:.1f}" text-anchor="end">{fmt(tv)}</text>')
        n = len(cats)
        if t == "bar":
            band = pw / n; bw = min(72, band * 0.62 / len(series))
            for ci, c in enumerate(cats):
                x0 = L + band * ci + (band - bw * len(series) - 3 * (len(series) - 1)) / 2
                cx = L + band * ci + band / 2
                lines = wrap(c, maxch)
                label = escape(c) if len(lines) == 1 else "".join(  # plain text keeps short-label output unchanged
                    f'<tspan x="{cx:.1f}" dy="{0 if k == 0 else 26}">{escape(ln)}</tspan>' for k, ln in enumerate(lines))
                parts.append(f'<text class="ch-tick" x="{cx:.1f}" y="{H-B+34}" text-anchor="middle">{label}</text>')
                for si, s in enumerate(series):
                    v = s["values"][ci]; h = ph * v / vmax; x = x0 + si * (bw + 3)
                    cls = f"ch-s{si+1}" + (" ch-mute" if focus is not None and c != focus else "")
                    parts.append(f'<path class="{cls}" d="{bar_path(x, top+ph-h, bw, h, 6)}"><title>{escape(c)} · {escape(s["name"])}: {fmt(v, unit)}</title></path>')
                    if mode == "all" or (mode == "max" and v == max(s["values"])) or c == focus:
                        parts.append(f'<text class="ch-value" x="{x+bw/2:.1f}" y="{top+ph-h-12:.1f}" text-anchor="middle">{fmt(v, unit)}</text>')
        else:  # line
            step = pw / max(1, n - 1)
            for ci, c in enumerate(cats):
                if n <= 12 or ci % math.ceil(n / 12) == 0:
                    parts.append(f'<text class="ch-tick" x="{L+step*ci:.1f}" y="{H-B+34}" text-anchor="middle">{escape(c)}</text>')
            for si, s in enumerate(series):
                pts = [(L + step * i, top + ph - ph * v / vmax) for i, v in enumerate(s["values"])]
                d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
                if len(series) == 1:
                    parts.append(f'<path class="ch-s1 ch-area" d="{d} L{pts[-1][0]:.1f},{top+ph} L{L},{top+ph}Z"/>')
                parts.append(f'<path class="ch-s{si+1} ch-line" d="{d}"/>')
                for (x, y), c, v in zip(pts, cats, s["values"]):
                    parts.append(f'<circle class="ch-hit" cx="{x:.1f}" cy="{y:.1f}" r="16"><title>{escape(c)} · {escape(s["name"])}: {fmt(v, unit)}</title></circle>')
                ex, ey = pts[-1]
                parts.append(f'<circle class="ch-s{si+1} ch-dot" cx="{ex:.1f}" cy="{ey:.1f}" r="7"/>'
                             f'<text class="ch-value" x="{ex+16:.1f}" y="{ey+8:.1f}">{fmt(s["values"][-1], unit)}</text>')
        parts.append(f'<line class="ch-axis" x1="{L}" y1="{top+ph}" x2="{L+pw}" y2="{top+ph}"/>')
    title = escape(spec.get("title", "Gráfica"))
    return (f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="{title}"><title>{title}</title>'
            f'<desc>{escape(desc)}</desc>{"".join(parts)}</svg>')

DEMO = {"type": "bar", "title": "Inscritos por cuatrimestre", "categories": ["Ene–Abr", "May–Ago", "Sep–Dic"],
        "series": [{"name": "2025", "values": [820, 760, 910]}, {"name": "2026", "values": [880, 845, 1020]}]}

def main():
    if "--demo" in sys.argv or len(sys.argv) < 2:
        spec = DEMO
    else:
        with open(sys.argv[1], encoding="utf-8") as f:
            spec = json.load(f)
    sys.stdout.reconfigure(encoding="utf-8")
    print(chart(spec))


if __name__ == "__main__":
    main()
