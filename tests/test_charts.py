import json
import xml.etree.ElementTree as ET

import pytest

from cmx_teach.slides.charts import chart, main
from conftest import run_main


@pytest.mark.parametrize("kind", ["bar", "hbar", "line"])
def test_chart_types_produce_valid_svg(kind):
    svg = chart({"type": kind, "categories": ["a", "b", "c"], "series": [{"name": "s", "values": [1, 5, 3]}]})
    assert ET.fromstring(svg).tag.endswith("svg")


def test_demo_cli(monkeypatch, capsys):
    assert run_main(main, ["--demo"], monkeypatch) == 0
    assert ET.fromstring(capsys.readouterr().out).tag.endswith("svg")


def test_spec_file_and_series_truncated_to_four(tmp_path, monkeypatch, capsys):
    spec = {"type": "bar", "categories": ["a", "b"], "series": [{"name": f"s{i}", "values": [1, 2]} for i in range(6)]}
    f = tmp_path / "d.json"
    f.write_text(json.dumps(spec), encoding="utf-8")
    run_main(main, [f], monkeypatch)
    svg = capsys.readouterr().out
    assert "ch-s4" in svg and "ch-s5" not in svg
    ET.fromstring(svg)


def test_wrap_limits_to_three_lines():
    from cmx_teach.slides.charts import wrap
    assert wrap("uno dos tres cuatro cinco seis siete ocho", 8) == ["uno dos", "tres", "cuatro"]
    assert wrap("corto", 10) == ["corto"]


def test_wrapped_labels_use_tspans():
    svg = chart({"type": "bar", "categories": ["Enero Febrero", "Marzo Abril"], "series": [{"name": "s", "values": [1, 2]}], "width": 300})
    assert "<tspan" in svg and "ch-s1" in svg


def test_long_labels_switch_bar_to_hbar():
    cats = ["Programación estructurada", "Bases de datos relacionales", "Ingeniería de requisitos"] * 3
    svg = chart({"type": "bar", "categories": cats, "series": [{"name": "s", "values": [3, 4, 5] * 3}]})
    import re
    m = re.search(r'class="ch-axis" x1="([\d.]+)" y1="[\d.]+" x2="([\d.]+)"', svg)
    assert m.group(1) == m.group(2) and "<tspan" not in svg  # hbar has a vertical axis
    ET.fromstring(svg)


def test_label_true_means_all():
    svg = chart({"type": "bar", "label": True, "categories": ["a", "b"], "series": [{"name": "s", "values": [1, 2]}]})
    assert svg.count("ch-value") == 2


def test_single_line_bar_labels_have_no_tspan():
    svg = chart({"type": "bar", "categories": ["A", "B"], "series": [{"name": "s", "values": [1, 2]}]})
    assert ">A</text>" in svg and "<tspan" not in svg  # output unchanged for short labels
