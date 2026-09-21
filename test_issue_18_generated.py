"""
Test for GitHub issue #15: Change background color to navy.
Verifies style.css sets body background-color to the required navy color code.
"""
import re
from pathlib import Path

CSS_PATH = Path(__file__).parent / "style.css"
EXPECTED_COLOR = "#000080"


def _get_background_color() -> str:
    css = CSS_PATH.read_text()
    m = re.search(r"body\s*{[^}]*background-color:\s*(#[0-9a-fA-F]{3,6})", css)
    assert m, "Could not find a background-color declaration inside the body { } rule"
    return m.group(1).lower()


def test_background_is_navy():
    color = _get_background_color()
    assert color == EXPECTED_COLOR, f"Expected background-color {EXPECTED_COLOR}, got {color}"
