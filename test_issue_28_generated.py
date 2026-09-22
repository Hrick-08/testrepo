from pathlib import Path
import re

def _get_background_color():
    css = Path('style.css').read_text(encoding='utf-8')
    m = re.search(r'body\s*{[^}]*background-color:\s*([^;\n]+)', css, re.IGNORECASE)
    assert m, 'Could not find a background-color declaration inside the body { } rule'
    return m.group(1).strip().lower()

def test_background_color_changed_to_green_issue_28():
    """Issue #28: Change the background color to green /SWEPilot

    This test checks that the body background-color in style.css has been
    changed to a green value. Several common representations are accepted.
    """
    color = _get_background_color()
    acceptable = {"#008000", "green", "#0a0", "#00ff00", "#0f0"}
    assert color in acceptable, f'Expected background color to be green, got: {color!r}'