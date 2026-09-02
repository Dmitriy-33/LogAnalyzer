from src.log_analyzer.stats import compute_stats

def test_compute_stats_basic():
    rows = [
        ("/a", 0.1, ""),
        ("/a", 0.3, ""),
        ("/b", 0.5, ""),
    ]
    gen = ((u, t, l) for u, t, l in rows)
    result, total, errors = compute_stats(gen, report_size=10, parse_error_threshold=0.5)
    assert total == 3
    assert errors == 0
    assert len(result) == 2
    a_row = next(r for r in result if r["url"] == "/a")
    assert a_row["count"] == 2
    assert a_row["time_sum"] == 0.4
    assert a_row["time_avg"] == 0.2
