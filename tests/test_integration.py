"""Integration tests for the Most Active Cookie application.

These tests focus on CLI-specific functionality, process integration,
and end-to-end behavior that cannot be tested at the unit level.
"""

import subprocess
import sys
from pathlib import Path


class TestCLIIntegration:
    """Test CLI-specific functionality and process integration."""

    def test_main_success_scenario(self):
        """Test one representative successful execution scenario."""
        fixture_path = Path(__file__).parent / "fixtures" / "sample_log.csv"

        result = subprocess.run(
            [
                sys.executable,
                "src/main.py",
                "-f",
                str(fixture_path),
                "-d",
                "2018-12-09",
            ],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert result.stdout.strip() == "AtY0laUfhglK3lC7"
        assert result.stderr == ""

    def test_main_file_not_found(self):
        """Test main application with nonexistent file."""
        result = subprocess.run(
            [
                sys.executable,
                "src/main.py",
                "-f",
                "nonexistent.csv",
                "-d",
                "2018-12-09",
            ],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2
        assert "File not found" in result.stderr

    def test_main_invalid_date_format(self):
        """Test main application with invalid date format."""
        fixture_path = Path(__file__).parent / "fixtures" / "sample_log.csv"

        result = subprocess.run(
            [
                sys.executable,
                "src/main.py",
                "-f",
                str(fixture_path),
                "-d",
                "invalid-date",
            ],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 2
        assert "Invalid date format" in result.stderr
