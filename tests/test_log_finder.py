from pathlib import Path
import tempfile
from datetime import datetime
from src.log_analyzer.log_finder import find_latest_log

def test_find_latest_simple():
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir)
        (p / "nginx-access-ui.log-20170629.gz").touch()
        (p / "nginx-access-ui.log-20170630").touch()  # plain
        (p / "other.log").touch()

        info = find_latest_log(p)
        assert info is not None
        assert info.date == datetime(2017, 6, 30)
        assert not info.is_gzip
        assert "20170630" in info.path.name

def test_no_matching_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        p = Path(tmpdir)
        (p / "other.log").touch()
        assert find_latest_log(p) is None
