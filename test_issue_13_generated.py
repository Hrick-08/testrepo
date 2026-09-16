"""Auto-generated test for issue 13: Change the background color to pink."""
import re
from pathlib import Path

CSS_PATH = Path(__file__).parent / "style.css"
EXPECTED_BG = "#ffc0cb"

def _get_background_color() -> str:
    css = CSS_PATH.read_text()
    # Find background-color declaration and return its value (trimmed and lowercased)
    m = re.search(r"background-color:\s*([^;\n]+)", css, re.IGNORECASE)
    assert m, "Could not find a background-color declaration"
    return m.group(1).strip().lower()

def test_background_color_is_pink():
    color = _get_background_color()
    assert color == EXPECTED_BG, f"Expected background-color {EXPECTED_BG}, got {color}"
