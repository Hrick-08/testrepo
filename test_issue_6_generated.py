import re 
 
def test_background_is_cyan(): 
    # Read the stylesheet and ensure the background color is set to cyan 
    with open('style.css', 'r', encoding='utf-8') as f: 
        css = f.read() 
    # Look for a background-color property and assert it is cyan (either named or hex #00ffff) 
    m = re.search(r'background-color\s*:\s*([^;]+);', css) 
    assert m is not None, 'No background-color property found in style.css' 
    value = m.group(1).strip().lower() 
    assert value in ('cyan', '#00ffff', '#0ff'), f'background-color is not cyan (found {value})' 
