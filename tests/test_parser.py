from src.log_analyzer.parser import parse_line
import io


def test_parse_line_ok():
    line = '127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /path HTTP/1.1" 200 1234 "-" "-" 0.123'
    url, time_val = parse_line(line)
    assert url == "/path"
    assert time_val == 0.123

def test_parse_line_bad():
    url, time_val = parse_line("invalid line")
    assert url is None
    assert time_val is None

def test_iter_log_lines():
    data = b'127.0.0.1 - - [...] "GET /a HTTP/1.1" 200 100 "-" "-" 0.2\n'
    f = io.BytesIO(data)
    res = list(iter_log_lines_mock(f, False))  # см. ниже
    assert len(res) == 1
    assert res[0][0] == "/a"
    assert res[0][1] == 0.2


def iter_log_lines_mock(fileobj, is_gzip: bool):
    import gzip
    from io import TextIOWrapper
    if is_gzip:
        f = TextIOWrapper(gzip.GzipFile(fileobj=fileobj), encoding="utf-8", errors="replace")
    else:
        f = io.TextIOWrapper(fileobj, encoding="utf-8", errors="replace")
    for raw_line in f:
        line = raw_line.strip()
        if not line:
            continue
        url, time_val = parse_line(line)
        yield url, time_val, line
