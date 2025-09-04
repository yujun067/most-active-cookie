"""Tests for the CLI module."""

import pytest
import tempfile
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from arg_parser import ArgumentParser  # noqa: E402 # type: ignore


class TestArgumentParsing:
    """Test argument parsing functionality."""

    def setup_method(self):
        """Setup method to create parser instance for each test."""
        self.parser = ArgumentParser()

    def create_test_file(self) -> str:
        """Create a test file for argument parsing tests."""
        temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False)
        temp_file.write("cookie,timestamp\ntest,2018-12-09T14:19:00+00:00")
        temp_file.close()
        return temp_file.name

    def test_parse_arguments_valid(self):
        """Test parsing valid arguments."""
        filename = self.create_test_file()

        try:
            args = self.parser.parse_arguments(["-f", filename, "-d", "2018-12-09"])

            assert args.filename == filename
            assert args.date == "2018-12-09"
            assert args.verbose is False
        finally:
            Path(filename).unlink()

    def test_parse_arguments_with_verbose(self):
        """Test parsing arguments with verbose flag."""
        filename = self.create_test_file()

        try:
            args = self.parser.parse_arguments(
                ["-f", filename, "-d", "2018-12-09", "--verbose"]
            )

            assert args.filename == filename
            assert args.date == "2018-12-09"
            assert args.verbose is True
        finally:
            Path(filename).unlink()

    def test_parse_arguments_missing_required(self):
        """Test parsing with missing required arguments."""
        # Missing filename
        with pytest.raises(SystemExit):
            self.parser.parse_arguments(["-d", "2018-12-09"])

        # Missing date
        filename = self.create_test_file()
        try:
            with pytest.raises(SystemExit):
                self.parser.parse_arguments(["-f", filename])
        finally:
            Path(filename).unlink()

    def test_parse_arguments_long_form(self):
        """Test parsing with long-form arguments."""
        filename = self.create_test_file()

        try:
            args = self.parser.parse_arguments(
                ["--filename", filename, "--date", "2018-12-09"]
            )

            assert args.filename == filename
            assert args.date == "2018-12-09"
        finally:
            Path(filename).unlink()
