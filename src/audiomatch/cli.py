import argparse

from audiomatch.match import match


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument("--length", type=int, default=120)
    args = parser.parse_args()

    match(args.path, args.length)
