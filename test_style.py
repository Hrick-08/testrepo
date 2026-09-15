"""
Simple test suite for the demo repo.
The agent's job is to make this test pass by editing style.css.

Run with: pytest test_style.py -v
"""
import re
from pathlib import Path

CSS_PATH = Path(__file__).parent / "style.css"
OLD_COLOR = "#ffffff"
EXPECTED_NEW_COLOR = "#ff0000"  # blue — the color requested in the current task


def _get_background_color() -> str:
    css = CSS_PATH.read_text()
    match = re.search(r"body\s*{[^}]*background-color:\s*(#[0-9a-fA-F]{3,6})", css)
    assert match, "Could not find a background-color declaration inside the body { } rule"
    return match.group(1).lower()


def test_background_color_was_changed_from_default():
    color = _get_background_color()
    assert color != OLD_COLOR, (
        f"background-color is still the original {OLD_COLOR} — issue not resolved"
    )


def test_background_color_matches_requested_value():
    color = _get_background_color()
    assert color == EXPECTED_NEW_COLOR, (
        f"Expected background-color {EXPECTED_NEW_COLOR}, got {color}"
    )
