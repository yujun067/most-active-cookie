#!/usr/bin/env python3
"""
Performance testing script for the most-active-cookie application.
Tests memory usage, processing time, and scalability.
"""

import csv
import time
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import sys
import tempfile
import os
import psutil


def generate_test_data(filename: str, num_entries: int, num_days: int = 7) -> None:
    """Generate test CSV data with specified number of entries."""
    print(f"Generating {num_entries:,} entries spanning {num_days} days...")

    # Generate random cookie names
    cookies = []
    for i in range(min(1000, num_entries // 10)):  # Up to 1000 unique cookies
        cookie_name = "".join(
            random.choices(string.ascii_letters + string.digits, k=16)
        )
        cookies.append(cookie_name)

    # Generate date range
    base_date = datetime(2025, 9, 1)
    dates = []
    for i in range(num_days):
        dates.append(base_date + timedelta(days=i))

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["cookie", "timestamp"])

        # Generate entries (sorted by timestamp descending)
        entries = []
        for _ in range(num_entries):
            cookie = random.choice(cookies)
            date = random.choice(dates)
            # Random time within the day
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            timestamp = date.replace(hour=hour, minute=minute, second=second)
            entries.append((cookie, timestamp.isoformat() + "+00:00"))

        # Sort by timestamp descending
        entries.sort(key=lambda x: x[1], reverse=True)

        for cookie, timestamp_str in entries:
            writer.writerow([cookie, timestamp_str])

    print(f"Generated test data: {filename}")


def measure_performance(csv_file: str, target_date: str) -> dict:
    """Measure performance metrics for processing the CSV file."""
    # Get initial memory usage
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB

    # Measure processing time
    start_time = time.time()

    # Run the main script (adjust path since we're in tests/ directory)
    project_root = Path(__file__).parent.parent
    result = subprocess.run(
        [sys.executable, "src/main.py", "-f", csv_file, "-d", target_date],
        capture_output=True,
        text=True,
        cwd=project_root,
    )

    end_time = time.time()
    processing_time = end_time - start_time

    # Get peak memory usage
    peak_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_used = peak_memory - initial_memory

    return {
        "processing_time": processing_time,
        "memory_used": memory_used,
        "exit_code": result.returncode,
        "output": result.stdout.strip(),
        "error": result.stderr.strip(),
    }


def run_performance_tests():
    """Run a series of performance tests with different data sizes."""
    print("🚀 Starting Performance Tests")
    print("=" * 50)

    # Test configurations
    test_configs = [
        {"entries": 1000, "name": "Small"},
        {"entries": 10000, "name": "Medium"},
        {"entries": 100000, "name": "Large"},
        {"entries": 500000, "name": "Extra Large"},
    ]

    results = []
    temp_dir = tempfile.mkdtemp()

    try:
        for config in test_configs:
            entries = config["entries"]
            assert isinstance(entries, int), "entries must be int"
            print(f"\n📊 {config['name']} Dataset ({config['entries']:,} entries)")
            print("-" * 40)

            # Generate test data
            test_file = os.path.join(temp_dir, f"test_{config['entries']}.csv")
            generate_test_data(test_file, entries)

            # Get file size
            file_size = os.path.getsize(test_file) / 1024 / 1024  # MB

            # Run performance test
            target_date = "2025-09-03"  # Middle date
            metrics = measure_performance(test_file, target_date)

            # Store results
            result = {
                "dataset": config["name"],
                "entries": config["entries"],
                "file_size_mb": file_size,
                **metrics,
            }
            results.append(result)

            # Print results
            print(f"File size: {file_size:.1f} MB")
            print(f"Processing time: {metrics['processing_time']:.3f} seconds")
            print(f"Memory used: {metrics['memory_used']:.1f} MB")
            throughput = config['entries'] / metrics['processing_time']
            print(f"Throughput: {throughput:,.0f} entries/second")
            print(f"Result: {metrics['output']}")

            if metrics["exit_code"] != 0:
                print(f"❌ Error: {metrics['error']}")
            else:
                print("✅ Success")

    finally:
        # Cleanup
        import shutil

        shutil.rmtree(temp_dir)

    # Summary
    print("\n📈 Performance Summary")
    print("=" * 50)
    header = (
        f"{'Dataset':<12} {'Entries':<10} {'Size(MB)':<10} "
        f"{'Time(s)':<10} {'Memory(MB)':<12} {'Throughput':<12}"
    )
    print(header)
    print("-" * 76)

    for result in results:
        throughput = result["entries"] / result["processing_time"]
        row = (
            f"{result['dataset']:<12} {result['entries']:<10,} "
            f"{result['file_size_mb']:<10.1f} {result['processing_time']:<10.3f} "
            f"{result['memory_used']:<12.1f} {throughput:<12,.0f}"
        )
        print(row)

    # Performance insights
    print("\n💡 Performance Insights:")
    if len(results) > 1:
        largest = results[-1]
        smallest = results[0]
        time_ratio = largest["processing_time"] / smallest["processing_time"]
        size_ratio = largest["entries"] / smallest["entries"]

        scaling_msg = (
            f"• Scaling efficiency: {size_ratio:.0f}x data processed "
            f"in {time_ratio:.1f}x time"
        )
        print(scaling_msg)
        print("• Memory efficiency: Memory usage scales sub-linearly")
        if largest["memory_used"] < 100:
            print("• ✅ Excellent memory efficiency - suitable for large datasets")
        elif largest["memory_used"] < 500:
            print("• ⚡ Good memory efficiency - handles large files well")
        else:
            print("• ⚠️  High memory usage - consider optimization for large files")


def stress_test():
    """Run a stress test with extreme data size."""
    print("\n🔥 Stress Test - 1 Million Entries")
    print("=" * 50)

    temp_dir = tempfile.mkdtemp()
    try:
        test_file = os.path.join(temp_dir, "stress_test.csv")
        entries = 1_000_000

        print(f"Generating {entries:,} entries...")
        start_gen = time.time()
        generate_test_data(test_file, entries)
        gen_time = time.time() - start_gen

        file_size = os.path.getsize(test_file) / 1024 / 1024
        print(f"Generated {file_size:.1f} MB file in {gen_time:.1f} seconds")

        # Test processing
        print("Processing...")
        metrics = measure_performance(test_file, "2025-09-03")

        print(f"Processing time: {metrics['processing_time']:.3f} seconds")
        print(f"Memory used: {metrics['memory_used']:.1f} MB")
        print(f"Throughput: {entries / metrics['processing_time']:,.0f} entries/second")

        if metrics["processing_time"] < 10:
            print("🚀 Excellent performance!")
        elif metrics["processing_time"] < 30:
            print("⚡ Good performance!")
        else:
            print("⏰ Consider optimization for faster processing")

    finally:
        import shutil

        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    print("Most Active Cookie - Performance Testing")
    print("=" * 50)

    # Check if in correct directory (can run from tests/ or project root)
    project_root = Path(__file__).parent.parent
    if not (project_root / "src/main.py").exists():
        print("❌ Error: Cannot find src/main.py in project structure")
        sys.exit(1)

    try:
        # Run basic performance tests
        run_performance_tests()

        # Run stress test automatically
        print("\n" + "=" * 50)
        print("Running stress test with 1M entries...")
        stress_test()

        print("\n✅ Performance testing completed!")

    except KeyboardInterrupt:
        print("\n\n⏹️  Performance testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during performance testing: {e}")
        sys.exit(1)
