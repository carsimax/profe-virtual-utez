import json
import shutil
import struct
from pathlib import Path

from cmx_teach.docs.visuals import main
from conftest import run_main

FIX = Path(__file__).parent / "fixtures/visuals"


def png_size(p):
    d = p.read_bytes()
    assert d[:8] == b"\x89PNG\r\n\x1a\n"
    return struct.unpack(">II", d[16:24])


def test_no_inputs_exits_2(tmp_path, monkeypatch):
    assert run_main(main, [tmp_path], monkeypatch) == 2


def test_unknown_preset_exits_2(tmp_path, monkeypatch):
    assert run_main(main, [tmp_path, "--preset", "nope"], monkeypatch) == 2


def test_chart_json_to_png(chromium, tmp_path, monkeypatch, capsys):
    shutil.copy(FIX / "avance.chart.json", tmp_path)
    assert run_main(main, [tmp_path, "--preset", "utez"], monkeypatch) == 0
    png = tmp_path / "avance.png"
    w, h = png_size(png)
    assert w >= 2000 and h > 600  # 1000px chart + padding at 2x scale
    assert "✔" in capsys.readouterr().out


def test_mmd_to_png(chromium, online, tmp_path, monkeypatch):
    f = tmp_path / "d.mmd"
    f.write_text("flowchart TB\n  A[Inicio] --> B[Fin]\n", encoding="utf-8")
    assert run_main(main, [f], monkeypatch) == 0
    assert png_size(tmp_path / "d.png")[0] >= 1800


def test_golden_mmd_and_charts_directory(chromium, online, tmp_path, monkeypatch):
    for f in FIX.glob("*.mmd"):
        shutil.copy(f, tmp_path)
    for f in FIX.glob("*.chart.json"):
        shutil.copy(f, tmp_path)
    assert run_main(main, [tmp_path, "--preset", "apa"], monkeypatch) == 0
    assert {p.name for p in tmp_path.glob("*.png")} == {"herencia.png", "avance.png", "evaluacion.png"}
