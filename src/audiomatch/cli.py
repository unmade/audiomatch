import argparse
import pathlib

from audiomatch.match import match


def main():
    parser = argparse.ArgumentParser(prog="audiomatch")
    parser.add_argument("path", type=pathlib.Path, nargs="+")
    parser.add_argument("--length", type=int, default=120)
    args = parser.parse_args()

    match(*args.path, length=args.length)
