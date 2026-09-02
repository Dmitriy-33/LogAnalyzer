import gzip
from pathlib import Path
from typing import Iterable, Tuple

def open_log(path: Path, is_gzip: bool):
    return gzip.open(path, "rt", encoding="utf-8", errors="replace") if is_gzip else path.open("r", encoding="utf-8", errors="replace")

def parse_line(line: str) -> Tuple[str | None, float | None]:

    first_quote = line.find('"')
    if first_quote == -1:
        return None, None
    second_quote = line.find('"', first_quote + 1)
    if second_quote == -1:
        return None, None

    request = line[first_quote+1:second_quote]
    parts = request.split()
    if len(parts) < 2:
        return None, None
    method, url, *_ = parts
    if method not in ("GET", "POST", "PUT", "DELETE", "HEAD"):
        return None, None

    last_field = line.strip().split()[-1]
    try:
        time_val = float(last_field)
    except ValueError:
        return None, None

    return url, time_val

def iter_log_lines(path: Path, is_gzip: bool) -> Iterable[Tuple[str | None, float | None, str]]:
    with open_log(path, is_gzip) as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            url, time_val = parse_line(line)
            yield url, time_val, line
