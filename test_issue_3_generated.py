from pathlib import Path 
import re 
 
CSS_PATH = Path(__file__).parent / "style.css"  
EXPECTED_COLOR = "#ff0000"  
OLD_COLOR = "#ffffff"  
  
def _get_text_color():  
    css = CSS_PATH.read_text(encoding="utf-8")  
    m = re.search(r"body\s*{[^}]*color:\s*(#[0-9a-fA-F]{3,6})", css)  
    assert m, "Could not find a color declaration inside the body { } rule"  
    return m.group(1).lower()  
  
def test_text_color_is_red():  
    assert _get_text_color() == EXPECTED_COLOR  
  
def test_text_color_was_changed_from_default():  
    assert _get_text_color() != OLD_COLOR  
