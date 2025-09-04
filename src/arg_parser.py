"""Command line interface for the most active cookie finder."""

import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional


class ArgumentParser:
    """Command line argument parser for the cookie finder application."""

    def __init__(self) -> None:
        """Initialize the argument parser with all required arguments."""
        self.parser = argparse.ArgumentParser(
            description="Find the most active cookie for a specific date",
            epilog="Example: %(prog)s -f cookie_log.csv -d 2018-12-09",
        )
        self._setup_arguments()

    def _setup_arguments(self) -> None:
        """Setup all command line arguments."""
        self.parser.add_argument(
            "-f",
            "--filename",
            type=self.validate_file_exists,
            required=True,
            help="Path to the cookie log CSV file",
        )

        self.parser.add_argument(
            "-d",
            "--date",
            type=self.validate_date_format,
            required=True,
            help="Target date in YYYY-MM-DD format",
        )

        self.parser.add_argument(
            "--verbose", "-v", action="store_true", help="Enable verbose output"
        )

    def validate_date_format(self, date_string: str) -> str:
        """Validate that the date string is in YYYY-MM-DD format.

        Args:
            date_string: Date string to validate

        Returns:
            The validated date string

        Raises:
            argparse.ArgumentTypeError: If date format is invalid
        """
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return date_string
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Invalid date format: {date_string}. Expected YYYY-MM-DD"
            )

    def validate_file_exists(self, file_path: str) -> str:
        """Validate that the file exists and is readable.

        Args:
            file_path: Path to the file to validate

        Returns:
            The validated file path

        Raises:
            argparse.ArgumentTypeError: If file doesn't exist or isn't readable
        """
        path = Path(file_path)
        if not path.exists():
            raise argparse.ArgumentTypeError(f"File not found: {file_path}")
        if not path.is_file():
            raise argparse.ArgumentTypeError(f"Path is not a file: {file_path}")
        if not path.stat().st_size > 0:
            raise argparse.ArgumentTypeError(f"File is empty: {file_path}")

        return file_path

    def parse_arguments(self, args: Optional[list] = None) -> argparse.Namespace:
        """Parse command line arguments.

        Args:
            args: Optional list of arguments (used for testing)

        Returns:
            Parsed arguments namespace
        """
        return self.parser.parse_args(args)
