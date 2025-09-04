#!/usr/bin/env python3
"""
Most Active Cookie Finder

A command-line tool to find the most active cookie for a specific date
from a cookie log file.

Usage:
    python src/main.py -f cookie_log.csv -d 2018-12-09

"""

import sys

from arg_parser import ArgumentParser  # type: ignore
from cookie_log_processor import CookieLogProcessor  # type: ignore
from logging_config import setup_logging  # type: ignore


def main() -> int:
    """Main entry point for the CLI application.

    Returns:
        Exit code (0 for success, 1 for runtime errors, 2 for usage errors)
    """
    try:
        argument_parser = ArgumentParser()
        args = argument_parser.parse_arguments()

        # Setup global logging configuration early
        setup_logging(args.verbose)

        processor = CookieLogProcessor(args.filename, args.date)
        most_active_cookies = processor.process()

        if most_active_cookies:
            for cookie in most_active_cookies:
                print(cookie)

        return 0

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
