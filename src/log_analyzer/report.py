import json
from pathlib import Path
from string import Template

def render_report(rows: list, template_path: Path, output_path: Path):
    with template_path.open("r", encoding="utf-8") as f:
        template_text = f.read()
    t = Template(template_text)
    table_json = json.dumps(rows, ensure_ascii=False)
    html = t.safe_substitute(table_json=table_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(html)
