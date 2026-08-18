"""Produce reproducible CPU and memory profiling evidence."""

from __future__ import annotations

import argparse
import cProfile
import csv
import json
import pstats
import time
import tracemalloc
from pathlib import Path
from typing import Callable

from analyzer import analyze_baseline, analyze_optimized, iter_flight_log


Analyzer = Callable[[object], dict[str, object]]


def profile_analyzer(
    name: str,
    analyzer: Analyzer,
    record_count: int,
    output_dir: Path,
) -> tuple[dict[str, object], dict[str, float]]:
    profiler = cProfile.Profile()
    tracemalloc.start()
    started = time.perf_counter()
    profiler.enable()
    summary = analyzer(iter_flight_log(record_count))
    profiler.disable()
    elapsed = time.perf_counter() - started
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    profiler.dump_stats(output_dir / f"{name}.prof")
    with (output_dir / f"profile_{name}.txt").open("w", encoding="utf-8") as stream:
        stats = pstats.Stats(profiler, stream=stream)
        stats.strip_dirs().sort_stats("cumulative").print_stats(20)

    metrics = {
        "elapsed_seconds": elapsed,
        "peak_memory_mib": peak / (1024 * 1024),
    }
    return summary, metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", type=int, default=50000)
    parser.add_argument("--out", type=Path, default=Path("results"))
    args = parser.parse_args()
    if args.records <= 0:
        raise SystemExit("--records must be positive")

    args.out.mkdir(parents=True, exist_ok=True)
    baseline_summary, baseline = profile_analyzer(
        "baseline", analyze_baseline, args.records, args.out
    )
    optimized_summary, optimized = profile_analyzer(
        "optimized", analyze_optimized, args.records, args.out
    )
    if baseline_summary != optimized_summary:
        raise RuntimeError("optimized implementation changed the business result")

    speedup = baseline["elapsed_seconds"] / optimized["elapsed_seconds"]
    memory_reduction = baseline["peak_memory_mib"] / optimized["peak_memory_mib"]
    rows = [
        {"implementation": "baseline", **baseline},
        {"implementation": "optimized", **optimized},
    ]
    with (args.out / "comparison.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    report = {
        "record_count": args.records,
        "business_summary": baseline_summary,
        "baseline": baseline,
        "optimized": optimized,
        "speedup_times": speedup,
        "peak_memory_reduction_times": memory_reduction,
    }
    (args.out / "summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
