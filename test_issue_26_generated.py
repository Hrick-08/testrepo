from pathlib import Path
import re


def _get_background_color():
    css = Path('style.css').read_text(encoding='utf-8')
    m = re.search('body\s*\{[^}]*background-color:\s*([^;\n]+)', css, re.IGNORECASE)
    assert m, 'Could not find a background-color declaration inside the body { } rule'
    return m.group(1).strip().lower()


def test_background_color_changed_to_pink():
    color = _get_background_color()
    # Accept common pink representations
    acceptable = {"pink", "#ffc0cb", "#ff69b4", "#f0f", "#ff1493"}
    assert color in acceptable, f'Expected background color to be pink, got: {color!r}'
