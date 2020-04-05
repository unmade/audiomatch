import argparse
import pathlib
import sys

from audiomatch import match, reports
from audiomatch.constants import DEFAULT_EXTENSIONS, DEFAULT_LENGTH
from audiomatch.exceptions import NotEnoughFiles


def invoke():
    parser = get_parser()
    args = parser.parse_args()

    try:
        matches = match.match(*args.path, length=args.length, extensions=args.extension)
    except NotEnoughFiles as exc:
        sys.exit(exc)

    reports.console(matches)


def get_parser():
    parser = argparse.ArgumentParser(
        prog="audiomatch",
        description="Compare audio files in a provided paths and show similar ones",
    )
    parser.add_argument(
        "path",
        type=pathlib.Path,
        nargs="+",
        help="filepath, glob-style pattern or a directory",
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=DEFAULT_LENGTH,
        metavar="SECONDS",
        help=f"""
            specifies how many seconds of the input audio to take for analysis
            (default: {DEFAULT_LENGTH})
        """,
    )
    parser.add_argument(
        "-e",
        "--extension",
        action="append",
        help=f"""
            Take only files with given extension
            (default: {', '.join(DEFAULT_EXTENSIONS)})
        """,
    )
    return parser
