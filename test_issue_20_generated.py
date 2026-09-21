"""
Test for issue #20: Change the background color to purple

This test verifies that style.css has background-color set to the requested
purple color (#800080) and that it was changed from the previous default.
"""
import re
from pathlib import Path

CSS_PATH = Path(__file__).parent / "style.css"
OLD_COLOR = "#000080"
EXPECTED_NEW_COLOR = "#800080"


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


def test_background_color_is_purple():
    color = _get_background_color()
    assert color == EXPECTED_NEW_COLOR, (
        f"Expected background-color {EXPECTED_NEW_COLOR}, got {color}"
    )
