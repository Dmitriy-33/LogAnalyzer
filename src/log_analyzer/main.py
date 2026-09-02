import argparse
import signal
import sys
from pathlib import Path

from .config import load_config
from .log_finder import find_latest_log
from .parser import iter_log_lines
from .stats import compute_stats
from .report import render_report
from .logger import configure_logger, get_logger


def handle_sigint(signum, frame):
    logger = get_logger()
    logger.error("interrupt")
    sys.exit(130)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=None, help="Path to config JSON")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
        sys.exit(1)

    log_path_opt = config.get("LOG_FILE")
    configure_logger(Path(log_path_opt) if log_path_opt else None)
    logger = get_logger()

    signal.signal(signal.SIGINT, handle_sigint)

    log_dir = Path(config["LOG_DIR"])
    report_dir = Path(config["REPORT_DIR"])
    report_size = int(config["REPORT_SIZE"])
    threshold = float(config["PARSE_ERROR_THRESHOLD"])

    latest_log = find_latest_log(log_dir)
    if latest_log is None:
        logger.info("no_logs")
        return 0

    date_str = latest_log.date.strftime("%Y.%m.%d")
    report_name = f"report-{date_str}.html"
    report_path = report_dir / report_name
    if report_path.exists():
        log_mtime = latest_log.path.stat().st_mtime
        report_mtime = report_path.stat().st_mtime
        if report_mtime >= log_mtime:
            logger.info("idempotent_skip", report=str(report_path))
            return 0

    logger.info("start", log_file=str(latest_log.path), is_gzip=latest_log.is_gzip)

    try:
        log_iter = iter_log_lines(latest_log.path, latest_log.is_gzip)
        rows, total_requests, parse_errors = compute_stats(
            log_iter, report_size, threshold
        )

        if total_requests > 0 and parse_errors / total_requests > threshold:
            logger.error(
                "parse_error_threshold_exceeded",
                parse_errors=parse_errors,
                total_requests=total_requests,
                threshold=threshold,
            )
            sys.exit(2)

        ROOT_DIR = Path(__file__).resolve().parents[2]
        template_path = ROOT_DIR / "templates" / "report.html"
        render_report(rows, template_path, report_path)

        logger.info(
            "report_generated",
            report=str(report_path),
            urls_count=len(rows),
            total_requests=total_requests,
            parse_errors=parse_errors,
        )
    except Exception as e:
        logger.error("unexpected_error", error=str(e), exc_info=True)
        sys.exit(3)

if __name__ == "__main__":
    main()
