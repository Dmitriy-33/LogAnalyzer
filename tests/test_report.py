from pathlib import Path
import tempfile
from src.log_analyzer.report import render_report

def test_render_report():
    rows = [{"url": "/a", "count": 1, "count_perc": 10.0, "time_sum": 0.5,
             "time_perc": 50.0, "time_avg": 0.5, "time_max": 0.5, "time_med": 0.5}]
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = Path(tmpdir)
        template = out_dir / "report.html"
        template.write_text('<html><body><script>$table_json</script></body></html>')
        output = out_dir / "out.html"
        render_report(rows, template, output)
        content = output.read_text(encoding="utf-8")
        assert '"url": "/a"' in content
        assert "$table_json" not in content  # заменён
