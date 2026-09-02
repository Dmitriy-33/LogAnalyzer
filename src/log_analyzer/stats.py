from collections import defaultdict
from collections.abc import Iterable
from statistics import median
from typing import Dict, List, Tuple

Row = Dict[str, any]

def compute_stats(
    log_iter: Iterable[Tuple[str | None, float | None, str]],
    report_size: int,
    parse_error_threshold: float
) -> Tuple[List[Row], int, int]:

    url_times: Dict[str, List[float]] = defaultdict(list)
    total_requests = 0
    parse_errors = 0

    for url, time_val, _ in log_iter:
        total_requests += 1
        if url is None or time_val is None:
            parse_errors += 1
            continue
        url_times[url].append(time_val)

    if total_requests > 0 and parse_errors / total_requests > parse_error_threshold:
        pass

    rows: List[Row] = []
    total_time = sum(sum(times) for times in url_times.values())

    sorted_urls = sorted(
        url_times.items(),
        key=lambda x: sum(x[1]),
        reverse=True
    )

    top_urls = sorted_urls[:report_size]

    for url, times in top_urls:
        count = len(times)
        time_sum = sum(times)
        time_avg = time_sum / count if count else 0.0
        time_max = max(times) if times else 0.0
        time_med = median(times) if times else 0.0

        count_perc = (count / total_requests * 100) if total_requests else 0.0
        time_perc = (time_sum / total_time * 100) if total_time else 0.0

        rows.append({
            "url": url,
            "count": count,
            "count_perc": round(count_perc, 2),
            "time_sum": round(time_sum, 3),
            "time_perc": round(time_perc, 2),
            "time_avg": round(time_avg, 3),
            "time_max": round(time_max, 3),
            "time_med": round(time_med, 3),
        })

    return rows, total_requests, parse_errors
