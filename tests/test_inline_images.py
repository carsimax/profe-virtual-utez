import base64

from cmx_teach.slides.inline_images import main
from conftest import run_main


def test_inline_only_real_local_src(tmp_path, monkeypatch):
    (tmp_path / "a.png").write_bytes(b"\x89PNGdata")
    (tmp_path / "lazy.png").write_bytes(b"lazy")
    html = tmp_path / "i.html"
    html.write_text(
        '<img src="a.png"><img src="http://x/y.png"><img src="data:image/png;base64,AA">'
        '<img src="missing.png"><img data-src="lazy.png">', encoding="utf-8")
    assert run_main(main, [html], monkeypatch) == 0
    s = html.read_text(encoding="utf-8")
    assert f'src="data:image/png;base64,{base64.b64encode(b"\x89PNGdata").decode()}"' in s
    assert 'src="http://x/y.png"' in s and 'src="data:image/png;base64,AA"' in s
    assert 'src="missing.png"' in s
    assert 'data-src="lazy.png"' in s
