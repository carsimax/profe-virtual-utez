"""QA of a .docx: structure checks + LibreOffice render to PDF/PNG + page map for the indices.
Usage: docs-qa documento.docx [--out qa/<nombre>] [--no-render]
Needs lxml; for render: LibreOffice (soffice) and poppler (pdftoppm, pdftotext, pdfinfo); Pillow for the contact sheet."""
import json, os, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
from lxml import etree

from .paths import qa_dir, sidecar

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def layout_warnings(xml, name_of, warnings):
    """House layout (non-APA): margins 1.5 cm (850 twips), fonts 9-11 pt, single line spacing.
    APA is detected by its Times New Roman default font (preset apa) and exempt."""
    styles = xml.get('word/styles.xml')
    if styles is None: return
    dflt = styles.find(f'{W}docDefaults/{W}rPrDefault/{W}rPr/{W}rFonts')
    if dflt is not None and dflt.get(W + 'ascii') == 'Times New Roman': return
    doc = xml['word/document.xml']
    for m in doc.iter(W + 'pgMar'):
        bad = [f'{k}={m.get(W + k)}' for k in ('top', 'bottom', 'left', 'right') if abs(int(m.get(W + k) or 0) - 850) > 10]
        if bad: warnings.append(f'Márgenes distintos de 1.5 cm (850 twips): {", ".join(bad)}'); break
    sizes, spacing = {}, {}
    for n, x in xml.items():
        if not re.match(r'word/(document|styles|header\d*|footer\d*|footnotes)\.xml', n): continue
        for el in x.iter(W + 'sz', W + 'szCs'):
            v = int(el.get(W + 'val') or 0)
            if 18 <= v <= 22: continue
            st, p, r = el, el, None
            while p is not None and p.tag not in (W + 'style', W + 'r', W + 'docDefaults'): p = p.getparent()
            if p is None: where = n
            elif p.tag == W + 'style': where = f'estilo “{name_of.get(p.get(W + "styleId"), p.get(W + "styleId"))}”'
            elif p.tag == W + 'docDefaults': where = 'valores predeterminados'
            else: where = f'texto “{"".join(t.text or "" for t in p.iter(W + "t"))[:30]}”'
            sizes.setdefault(where, v / 2)
        for sp in x.iter(W + 'spacing'):
            ln = sp.get(W + 'line')
            if ln is not None and (ln != '240' or sp.get(W + 'lineRule') not in (None, 'auto')):
                p = sp
                while p is not None and p.tag not in (W + 'style', W + 'p'): p = p.getparent()
                where = (f'estilo “{name_of.get(p.get(W + "styleId"), p.get(W + "styleId"))}”' if p is not None and p.tag == W + 'style'
                         else f'párrafo “{"".join(t.text or "" for t in p.iter(W + "t"))[:30]}”' if p is not None else n)
                spacing.setdefault(where, ln)
    if sizes: warnings.append('Tamaño de fuente fuera de 9-11 pt: ' + '; '.join(f'{k} ({v:g} pt)' for k, v in list(sizes.items())[:6]))
    if spacing: warnings.append('Interlineado distinto de sencillo (1.0): ' + '; '.join(f'{k} (line={v})' for k, v in list(spacing.items())[:6]))


def main():
    args = sys.argv[1:]
    if not args or args[0].startswith('--'):
        print('Uso: docs-qa documento.docx [--out DIR] [--no-render]', file=sys.stderr)
        sys.exit(2)
    src = Path(args[0]); out = Path(args[args.index('--out') + 1]) if '--out' in args else qa_dir(src)
    render = '--no-render' not in args
    problems, warnings, pending, info = [], [], [], []
    has_cover = False
    _ol = sidecar(src, '.outline.json')
    if _ol.exists(): has_cover = json.loads(_ol.read_text()).get('cover') not in (None, False, 'apa')

    # ── 1. estructura
    try: z = zipfile.ZipFile(src)
    except (zipfile.BadZipFile, OSError) as e: sys.exit(f'No es un .docx válido: {e}')
    xml = {}
    for n in z.namelist():
        if n.endswith('.xml') or n.endswith('.rels'):
            try: xml[n] = etree.fromstring(z.read(n))
            except Exception as e: problems.append(f'XML inválido en {n}: {e}')
    doc = xml.get('word/document.xml')
    if doc is None: sys.exit('No es un .docx válido (falta word/document.xml)')
    styles = xml.get('word/styles.xml')
    name_of = {s.get(W + 'styleId'): (s.find(W + 'name').get(W + 'val') if s.find(W + 'name') is not None else '') for s in styles.iter(W + 'style')} if styles is not None else {}
    def level(p):
        ps = p.find(f'{W}pPr/{W}pStyle')
        if ps is None: return None
        m = re.match(r'heading\s*(\d)', name_of.get(ps.get(W + 'val'), ps.get(W + 'val')).lower())
        return int(m.group(1)) if m else None
    text = lambda el: ''.join(t.text or '' for t in el.iter(W + 't'))
    prev, empties, n_heads = 0, 0, 0
    body = doc.find(W + 'body')
    for p in body.iter(W + 'p'):
        lv = level(p)
        if lv:
            n_heads += 1
            if prev and lv > prev + 1: problems.append(f'Salto de nivel de título (H{prev} → H{lv}) en “{text(p)[:50]}”')
            prev = lv
        t = text(p)
        if re.match(r'^\s*[•●▪◦\-–]\s', t) and p.find(f'{W}pPr/{W}numPr') is None and p.getparent().tag != W + 'tc':
            problems.append(f'Viñeta escrita a mano (usa listas reales): “{t[:50]}”')
        empties = empties + 1 if not t.strip() and p.find(f'.//{W}drawing') is None and p.find(f'.//{W}br') is None and p.getparent().tag == W + 'body' else 0
        if empties == 3: warnings.append('3+ párrafos vacíos seguidos: usa espaciado de párrafo, no Enter vacíos')
    alltext = '\n'.join(text(x) for n, x in xml.items() if n.startswith('word/') and n.endswith('.xml'))
    for pat, label in [(r'\{\{[^}]*\}\}|\{%[^%]*%\}', 'etiqueta de plantilla sin llenar'), (r'\[DATO PENDIENTE\]|\[CONFIRMAR\]|\[Nombre[^\]]*\]|\bTODO\b|\bTBD\b', 'dato pendiente'),
                       (r'(?i)lorem ipsum|xxxx', 'texto de relleno')]:
        found = re.findall(pat, alltext)
        for m in sorted(set(found))[:8]:
            ctx = [re.sub(r'\s+', ' ', x.group(0)).strip() for x in re.finditer(r'.{0,40}' + re.escape(m) + r'.{0,25}', alltext)][:4]
            pending.append(f'{label} “{m}” ×{found.count(m)}' + ''.join(f'\n    … {c}' for c in ctx))
    for d in doc.iter('{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}docPr'):
        if not (d.get('descr') or d.get('title')): warnings.append(f'Imagen sin texto alternativo ({d.get("name")})')
    for tbl in body.iter(W + 'tbl'):
        grid = [int(g.get(W + 'w') or 0) for g in tbl.findall(f'{W}tblGrid/{W}gridCol')]
        tw = tbl.find(f'{W}tblPr/{W}tblW')
        if tw is not None and tw.get(W + 'type') == 'dxa' and grid and abs(sum(grid) - int(tw.get(W + 'w'))) > 20:
            warnings.append(f'Tabla: columnas suman {sum(grid)} DXA pero la tabla mide {tw.get(W + "w")}')
        if tw is not None and tw.get(W + 'type') == 'pct': warnings.append('Tabla con ancho en porcentaje: usa DXA (se rompe en Google Docs)')
    fonts = {f.get(W + 'ascii') for x in xml.values() for f in x.iter(W + 'rFonts') if f.get(W + 'ascii')}
    if len(fonts) > 3: warnings.append(f'Demasiadas familias tipográficas: {", ".join(sorted(fonts))}')
    layout_warnings(xml, name_of, warnings)
    hf = [x for n, x in xml.items() if re.match(r'word/(footer|header)\d*\.xml', n)]
    if not any('PAGE' in (i.text or '') for f in hf for i in f.iter(W + 'instrText')) and not any(fl.get(W + 'instr', '').strip().startswith('PAGE') for f in hf for fl in f.iter(W + 'fldSimple')):
        warnings.append('Sin número de página real (campo PAGE) en encabezado ni pie')

    # ── 2. render
    pages = 0
    if render:
        soffice = shutil.which('soffice') or shutil.which('libreoffice') or next((p for p in ['/Applications/LibreOffice.app/Contents/MacOS/soffice', r'C:\Program Files\LibreOffice\program\soffice.exe'] if os.path.exists(p)), None)
        if not soffice: warnings.append('LibreOffice no disponible: no se generó PDF ni capturas (revisa visualmente en Word)')
        else:
            out.mkdir(parents=True, exist_ok=True)
            prof = tempfile.mkdtemp(prefix='lo_')
            env = {**os.environ, 'SAL_USE_VCLPLUGIN': 'svp'}
            r = subprocess.run([soffice, f'-env:UserInstallation=file://{prof}', '--headless', '--norestore', '--convert-to', 'pdf', '--outdir', str(out), str(src)],
                               capture_output=True, text=True, env=env, timeout=240)
            pdf = out / (src.stem + '.pdf')
            if not pdf.exists(): problems.append('LibreOffice no pudo abrir el documento: ' + (r.stderr or r.stdout).strip()[:200])
            else:
                pages = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True).stdout).group(1))
                for f in out.glob('page-*.png'): f.unlink()
                subprocess.run(['pdftoppm', '-png', '-r', '110', str(pdf), str(out / 'page')], check=True)
                try:
                    from PIL import Image
                    ims = [Image.open(f).convert('RGB') for f in sorted(out.glob('page-*.png'), key=lambda f: int(re.search(r'(\d+)', f.stem).group(1)))]
                    for i, im in enumerate(ims, 1):
                        g = im.convert('L').resize((60, 80)); ink = sum(g.histogram()[:235]) / 4800
                        if i == 1 and has_cover:
                            rows = [y for y in range(80) if min(g.getpixel((x, y)) for x in range(60)) < 235]
                            if rows and rows[-1] < 80 * 0.62: warnings.append(f'Portada ocupa solo {rows[-1] / 80:.0%} de la página: agrega datos (meta.fields, fecha, lugar) o más espacio')
                        if ink < 0.01: problems.append(f'Página {i} en blanco')
                        elif i == len(ims) and i > 1 and ink < 0.04: warnings.append(f'Última página casi vacía ({ink:.0%} de tinta): ajusta para no dejar una línea huérfana')
                    cols = 4; th = [im.resize((im.width * 70 // 110, im.height * 70 // 110)) for im in ims]; ims = th; w, h = ims[0].size
                    sheet = Image.new('RGB', (w * cols, h * ((len(ims) + cols - 1) // cols)), (255, 255, 255))
                    for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * w, (i // cols) * h))
                    sheet.save(out / 'sheet.png')
                except ImportError: warnings.append('Pillow no instalado: sin hoja de contactos (pip install pillow)')
                # mapa de páginas para índices
                outline = sidecar(src, '.outline.json')
                if outline.exists():
                    ol = json.loads(outline.read_text())
                    raw = subprocess.run(['pdftotext', '-layout', str(pdf), '-'], capture_output=True, text=True).stdout.split('\f')
                    norm = lambda s: re.sub(r'\s+', ' ', s).strip().lower()
                    labels = []
                    for pg in raw:
                        ls = [l.strip() for l in pg.strip().splitlines() if l.strip()]
                        lab = None
                        for l in reversed(ls[-3:]):                       # pie: “Página N”, “N” o romano
                            m = re.search(r'(?:página|page)\s+(\d+)', l, re.I) or re.fullmatch(r'(\d+)', l)
                            if m: lab = int(m.group(1)); break
                            if re.fullmatch(r'[ivxlc]+', l, re.I): lab = 'roman'; break
                        if lab is None and ls:                            # encabezado (APA): número al final de la primera línea
                            m = re.search(r'(?:^|\s)(\d+|[ivxlc]+)$', ls[0], re.I)
                            if m: lab = int(m.group(1)) if m.group(1).isdigit() else 'roman'
                        labels.append(lab)
                    bodypages = [(lab, norm(pg)) for lab, pg in zip(labels, raw) if isinstance(lab, int)]
                    pm = {'headings': {}, 'captions': {}}
                    bodylines = [(lab, [re.sub(r'^\d+(\.\d+)*\.?\s+', '', norm(l)) for l in pg.splitlines() if l.strip()]) for lab, pg in zip(labels, raw) if isinstance(lab, int)]
                    start = 0                                             # los títulos van en orden: busca hacia adelante
                    for h in ol['headings']:
                        k = norm(h['key'])
                        for j in range(start, len(bodylines)):
                            lab, ls = bodylines[j]
                            if k and any(l == k or (len(l) >= 12 and k.startswith(l)) for l in ls):
                                pm['headings'][h['key']] = lab; start = j; break
                    for c in ol['captions']:
                        pat = re.escape(norm(c['key'])) + r'[\s.:—-]*' + re.escape(norm(c['text'])[:24])
                        for lab, t in bodypages:
                            if re.search(pat, t): pm['captions'][c['key']] = lab; break
                    pj = sidecar(src, '.pages.json'); old = pj.read_text() if pj.exists() else ''
                    new = json.dumps(pm, ensure_ascii=False, indent=1); pj.write_text(new)
                    changed = new != old
                    miss = len(ol['headings']) - len(pm['headings']) + len(ol['captions']) - len(pm['captions'])
                    print(f'Mapa de páginas: {len(pm["headings"])} títulos, {len(pm["captions"])} leyendas' + (f' ({miss} sin ubicar)' if miss else '') +
                          f' → {pj.name}.' + (' CAMBIARON: vuelve a ejecutar docgen y este QA para escribir los números en los índices.' if changed and ol.get('hasIndex') else ' Sin cambios: índices al día.'))
            shutil.rmtree(prof, ignore_errors=True)

    print(f'{src.name}: {n_heads} títulos' + (f', {pages} páginas, capturas en {out}/' if pages else ''))
    for i in info: print(i)
    if pending: print('DATOS PENDIENTES (confírmalos con el usuario o déjalos visibles a propósito):\n- ' + '\n- '.join(pending))
    if warnings: print('REVISAR:\n- ' + '\n- '.join(dict.fromkeys(warnings)))
    if problems: print('PROBLEMAS:\n- ' + '\n- '.join(dict.fromkeys(problems))); sys.exit(1)
    print('OK')


if __name__ == "__main__":
    main()
