"""Core logic for processing cookie log files and finding most active cookies."""

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterator, List, Tuple

from logging_config import get_logger  # type: ignore


class CookieLogProcessor:
    """Processes cookie log files to find the most active cookie for a given date."""

    # Class variable - shared across all instances
    logger = get_logger(__name__)

    def __init__(self, filename: str, target_date: str):
        """Initialize the processor.

        Args:
            filename: Path to the cookie log CSV file
            target_date: Target date in YYYY-MM-DD format
        """
        self.filename = Path(filename)
        self.target_date = target_date
        self.logger.debug(
            f"Initialized processor for file: {filename}, date: {target_date}"
        )

    def process(self) -> List[str]:
        """Process the cookie log file and return the most active cookie(s).

        Returns:
            List of most active cookie names for the target date

        Raises:
            FileNotFoundError: If the log file doesn't exist
            ValueError: If the file format is invalid
        """
        self.logger.debug("Starting cookie log processing")

        try:
            cookie_counts = self._count_cookies_for_date()
            most_active = self._find_most_active(cookie_counts)

            self.logger.debug(f"Found {len(most_active)} most active cookie(s)")
            return most_active

        except Exception as e:
            self.logger.error(f"Error processing cookie log: {e}")
            raise

    def _read_cookie_log(self) -> Iterator[Tuple[str, str]]:
        """Read and parse the cookie log file.

        Yields:
            Tuples of (cookie_name, timestamp_string)

        Raises:
            FileNotFoundError: If the file doesn't exist
            csv.Error: If the CSV format is invalid
        """
        self.logger.debug(f"Reading cookie log from: {self.filename}")

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                reader = csv.reader(file)

                # Skip header row
                header = next(reader, None)
                if header is None:
                    raise ValueError("Empty file")

                expected_header = ["cookie", "timestamp"]
                if header != expected_header:
                    self.logger.warning(
                        f"Unexpected header: {header}, expected: {expected_header}"
                    )

                line_num = 2  # Start from line 2
                for row in reader:
                    if len(row) != 2:
                        self.logger.warning(
                            f"Skipping malformed line {line_num}: {row}"
                        )
                        line_num += 1
                        continue

                    cookie, timestamp = row[0].strip(), row[1].strip()
                    if not cookie or not timestamp:
                        self.logger.warning(f"Skipping empty values on line {line_num}")
                        line_num += 1
                        continue

                    yield cookie, timestamp
                    line_num += 1

        except FileNotFoundError:
            self.logger.error(f"File not found: {self.filename}")
            raise
        except csv.Error as e:
            self.logger.error(f"CSV parsing error: {e}")
            raise ValueError(f"Invalid CSV format: {e}")

    def _extract_date(self, timestamp_str: str) -> str:
        """Extract date in YYYY-MM-DD format from timestamp.

        Args:
            timestamp_str: Timestamp string in ISO format
                (e.g., 2018-12-09T14:19:00+00:00)

        Returns:
            Date string in YYYY-MM-DD format
        """
        try:
            dt = datetime.fromisoformat(timestamp_str)
        except ValueError as e:
            self.logger.warning(f"Invalid timestamp format: {timestamp_str}")
            raise ValueError(f"Invalid timestamp format: {timestamp_str}") from e

        return dt.date().isoformat()

    def _count_cookies_for_date(self) -> Dict[str, int]:
        """Count cookie occurrences for the target date.

        Returns:
            Dictionary mapping cookie names to their occurrence counts
        """
        self.logger.debug(f"Counting cookies for date: {self.target_date}")

        cookie_counts: Dict[str, int] = defaultdict(int)
        processed_entries = 0
        relevant_entries = 0

        for cookie, timestamp in self._read_cookie_log():
            processed_entries += 1

            try:
                entry_date = self._extract_date(timestamp)

                if entry_date == self.target_date:
                    cookie_counts[cookie] += 1
                    relevant_entries += 1
                    self.logger.debug(f"Found cookie '{cookie}' on target date")
                elif entry_date < self.target_date:
                    # Since data is sorted by timestamp descending,
                    # we can stop when we encounter dates before our target
                    self.logger.debug(
                        f"Reached date {entry_date} < {self.target_date}, stopping"
                    )
                    break

            except ValueError as e:
                self.logger.warning(f"Skipping entry with invalid timestamp: {e}")
                continue

        self.logger.debug(
            f"Processed {processed_entries} entries, "
            f"found {relevant_entries} for target date"
        )
        return cookie_counts

    def _find_most_active(self, cookie_counts: Dict[str, int]) -> List[str]:
        """Find the cookie(s) with the highest count.

        Args:
            cookie_counts: Dictionary mapping cookie names to counts

        Returns:
            List of cookie names with the highest count (handles ties)
        """
        if not cookie_counts:
            self.logger.debug("No cookies found for the target date")
            return []

        max_count = max(cookie_counts.values())
        most_active = [
            cookie for cookie, count in cookie_counts.items() if count == max_count
        ]

        self.logger.debug(f"Most active cookies (count={max_count}): {most_active}")
        return sorted(most_active)  # Sort for consistent output
