from pathlib import Path

def test_index_has_title_welcome():
    html = Path('index.html').read_text(encoding='utf-8')
    lower = html.lower()
    start = lower.find('<title>')
    end = lower.find('</title>', start)
    assert start != -1 and end != -1
    title = html[start+7:end].strip()
    assert title == 'Welcome', f"Expected title 'Welcome', got: {title!r}"
