"""House layout: 1.5 cm margins, 9-11 pt fonts, single spacing (apa exempt), enforced by docs-qa."""

import hashlib
import re
import shutil
import zipfile
from pathlib import Path

import pytest
from docx import Document
from docx.shared import Cm, Pt

from cmx_teach.docs.build import main as build
from cmx_teach.docs.qa import main as qa
from conftest import run_main

FIX = Path(__file__).parent / "fixtures" / "docs" / "build"
HOUSE = ["examen", "oficio", "planeacion", "srs"]
APA_SHA256 = "d10c20e9225e6a7cac8185e9d44e8c2b56c5c48bc050ef1002cb99973acb23a5"  # apa.json output; changed only by split field runs in header1/2.xml (layout values identical)


def built(tmp_path, monkeypatch, name):
    work = tmp_path / "w"
    if not work.exists():
        shutil.copytree(FIX, work)
    assert run_main(build, [work / f"{name}.json"], monkeypatch) == 0
    return work / f"{name}.docx"


def parts(docx):
    z = zipfile.ZipFile(docx)
    return {n: z.read(n).decode() for n in z.namelist() if re.match(r"word/(document|styles|stylesWithEffects|header\d*|footer\d*|footnotes)\.xml", n)}


@pytest.mark.parametrize("name", HOUSE)
def test_margins_are_1_5_cm(tmp_path, monkeypatch, name):
    doc = parts(built(tmp_path, monkeypatch, name))["word/document.xml"]
    margins = re.findall(r"<w:pgMar ([^>]*)/>", doc)
    assert margins
    for m in margins:
        assert {k: int(v) for k, v in re.findall(r'w:(top|right|bottom|left)="(\d+)"', m)} == dict(top=850, right=850, bottom=850, left=850)


@pytest.mark.parametrize("name", HOUSE)
def test_all_sizes_between_9_and_11_pt_and_single_spacing(tmp_path, monkeypatch, name):
    for part, x in parts(built(tmp_path, monkeypatch, name)).items():
        sizes = {int(v) for v in re.findall(r'<w:szC?s? w:val="(\d+)"', x)}
        assert sizes <= set(range(18, 23)), (part, sizes)
        for sp in re.findall(r"<w:spacing[^>]*w:line=[^>]*>", x):
            assert 'w:line="240"' in sp and 'w:lineRule="auto"' in sp, (part, sp)


@pytest.mark.parametrize("name", HOUSE)
def test_qa_quiet_on_build_output(tmp_path, monkeypatch, capsys, name):
    docx = built(tmp_path, monkeypatch, name)
    run_main(qa, [docx, "--no-render"], monkeypatch)
    out = capsys.readouterr().out
    assert "Márgenes" not in out and "fuera de 9-11" not in out and "Interlineado" not in out


def test_apa_output_unchanged(tmp_path, monkeypatch):
    assert hashlib.sha256(built(tmp_path, monkeypatch, "apa").read_bytes()).hexdigest() == APA_SHA256


def test_qa_flags_12pt_wide_margins_and_loose_spacing(tmp_path, monkeypatch, capsys):
    d = Document()
    s = d.sections[0]
    s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Cm(2.54)
    d.styles["Normal"].font.size = Pt(12)
    d.styles["Normal"].paragraph_format.line_spacing = 1.5
    p = d.add_paragraph("Texto de prueba")
    p.runs[0].font.size = Pt(12)
    f = tmp_path / "hecho-a-mano.docx"
    d.save(f)
    run_main(qa, [f, "--no-render"], monkeypatch)
    out = capsys.readouterr().out
    assert "Márgenes distintos de 1.5 cm" in out
    assert "Tamaño de fuente fuera de 9-11 pt" in out and "12 pt" in out
    assert "Interlineado distinto de sencillo" in out


@pytest.mark.parametrize("name", ["apa", "planeacion", "examen"])
def test_field_runs_are_split_and_carry_size(tmp_path, monkeypatch, name):
    for part, x in parts(built(tmp_path, monkeypatch, name)).items():
        if part == "word/stylesWithEffects.xml":
            continue
        for r in re.findall(r"<w:r>.*?</w:r>", x, re.S):
            assert not ('fldCharType="begin"' in r and 'fldCharType="end"' in r), part
    footer = [x for p, x in parts(built(tmp_path, monkeypatch, "planeacion")).items() if re.match(r"word/footer", p)]
    for x in footer:
        for r in re.findall(r"<w:r>.*?</w:r>", x, re.S):
            if "<w:t>" in r:  # every text run in the footer, field results included, has the footer size
                assert 'w:sz w:val="18"' in r, r


def test_footer_digits_same_height_as_text(tmp_path, monkeypatch):
    import subprocess
    soffice = shutil.which("soffice")
    if not soffice or not shutil.which("pdftoppm"):
        pytest.skip("LibreOffice/poppler missing")
    docx = built(tmp_path, monkeypatch, "examen")
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(tmp_path), str(docx)],
                   capture_output=True, stdin=subprocess.DEVNULL, timeout=240)
    out = subprocess.run(["pdftotext", "-bbox", "-f", "1", "-l", "1", str(tmp_path / "examen.pdf"), "-"],
                         capture_output=True, text=True).stdout
    words = re.findall(r'yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)">(Página|de|\d+)<', out)
    foot = [(w, float(b) - float(a)) for a, b, w in words if float(a) > 700]
    h = {w: v for w, v in foot}
    assert "Página" in h and "de" in h
    digits = [v for w, v in foot if w.isdigit()]
    assert digits and all(abs(v - h["Página"]) <= 0.7 for v in digits), foot


@pytest.mark.parametrize("preset", ["utez", "corporativo", "tecnico", "editorial"])
def test_heading3_is_bold_italic(tmp_path, monkeypatch, preset):
    work = tmp_path / "w"
    shutil.copytree(FIX, work)
    spec = work / "planeacion.json"
    import json
    d = json.loads(spec.read_text())
    d["preset"] = preset
    spec.write_text(json.dumps(d, ensure_ascii=False))
    assert run_main(build, [spec], monkeypatch) == 0
    st = parts(work / "planeacion.docx")["word/styles.xml"]
    h3 = re.search(r'<w:style [^>]*w:styleId="Heading3".*?</w:style>', st, re.S).group(0)
    assert "<w:b/>" in h3 and "<w:i/>" in h3
