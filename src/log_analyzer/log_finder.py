import re
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path

@dataclass
class LogInfo:
    path: Path
    date: datetime
    is_gzip: bool


LOG_PATTERN = re.compile(
    r"nginx[_-]access[_-]ui\.log[-_]?(\d{8}).*\.gz$"
)

def find_latest_log(log_dir: Path) -> LogInfo | None:
    latest: LogInfo | None = None
    for entry in log_dir.iterdir():
        if not entry.is_file():
            continue
        m = LOG_PATTERN.search(entry.name)
        if not m:
            continue
        date_str = m.group(1)
        is_gzip = entry.name.lower().endswith(".gz")
        try:
            dt = datetime.strptime(date_str, "%Y%m%d")
        except ValueError:
            continue
        info = LogInfo(path=entry, date=dt, is_gzip=is_gzip)
        if latest is None or dt > latest.date:
            latest = info
    return latest
