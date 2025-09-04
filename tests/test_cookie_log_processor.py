"""Tests for the CookieLogProcessor class."""

import pytest
from pathlib import Path
import sys

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from cookie_log_processor import CookieLogProcessor  # noqa: E402 # type: ignore


class TestCookieLogProcessor:
    """Test cases for CookieLogProcessor."""

    def test_extract_date_valid_timestamp(self):
        """Test extracting date from valid timestamp (tests internal parsing too)."""
        processor = CookieLogProcessor("dummy.csv", "2018-12-09")

        timestamp_str = "2018-12-09T14:19:00+00:00"
        result = processor._extract_date(timestamp_str)

        assert result == "2018-12-09"

    def test_extract_date_invalid_timestamp(self):
        """Test extracting date from invalid timestamp raises ValueError."""
        processor = CookieLogProcessor("dummy.csv", "2018-12-09")

        with pytest.raises(ValueError, match="Invalid timestamp format"):
            processor._extract_date("10-10-2025")

    def test_extract_date_different_timezone(self):
        """Test extracting date from timestamp with different timezone."""
        processor = CookieLogProcessor("dummy.csv", "2018-12-09")

        timestamp_str = "2018-12-09T23:19:00-05:00"
        result = processor._extract_date(timestamp_str)

        assert result == "2018-12-09"

        timestamp_str = "2018-12-09T23:19:00+00:00"
        result = processor._extract_date(timestamp_str)

        assert result == "2018-12-09"

    def test_find_most_active_single_winner(self):
        """Test finding most active cookie with single winner."""
        processor = CookieLogProcessor("dummy.csv", "2018-12-09")

        cookie_counts = {"cookie1": 3, "cookie2": 1, "cookie3": 2}

        result = processor._find_most_active(cookie_counts)
        assert result == ["cookie1"]

    def test_find_most_active_tie(self):
        """Test finding most active cookies with tie."""
        processor = CookieLogProcessor("dummy.csv", "2018-12-09")

        cookie_counts = {"cookie1": 3, "cookie2": 3, "cookie3": 1}

        result = processor._find_most_active(cookie_counts)
        assert set(result) == {"cookie1", "cookie2"}
        assert len(result) == 2

    def test_find_most_active_empty_data(self):
        """Test finding most active cookies with empty data."""
        processor = CookieLogProcessor("dummy.csv", "2018-12-09")

        cookie_counts: dict[str, int] = {}

        result = processor._find_most_active(cookie_counts)
        assert result == []


class TestCookieLogProcessorWithFiles:
    """Test cases that require actual files."""

    def test_process_sample_data(self):
        """Test processing the sample data from requirements."""
        fixture_path = Path(__file__).parent / "fixtures" / "sample_log.csv"
        processor = CookieLogProcessor(str(fixture_path), "2018-12-09")

        result = processor.process()
        assert result == ["AtY0laUfhglK3lC7"]

    def test_process_tie_scenario(self):
        """Test processing data with tied most active cookies."""
        fixture_path = Path(__file__).parent / "fixtures" / "tie_scenario.csv"
        processor = CookieLogProcessor(str(fixture_path), "2018-12-09")

        result = processor.process()
        # Both cookies should be returned in sorted order
        assert set(result) == {"AtY0laUfhglK3lC7", "SAZuXPGUrfbcn5UA"}

    def test_process_no_data_for_date(self):
        """Test processing when no data exists for target date."""
        fixture_path = Path(__file__).parent / "fixtures" / "tie_scenario.csv"
        processor = CookieLogProcessor(str(fixture_path), "2018-12-10")

        result = processor.process()
        assert result == []

    def test_process_malformed_csv_lines(self):
        """Test processing CSV with malformed lines."""
        fixture_path = (
            Path(__file__).parent / "fixtures" / "malformed_missing_fields.csv"
        )
        processor = CookieLogProcessor(str(fixture_path), "2018-12-09")

        result = processor.process()
        # Should process valid lines and ignore malformed ones
        assert result == ["AtY0laUfhglK3lC7"]
