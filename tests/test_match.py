from importlib import resources
from pathlib import Path

from audiomatch import match

SAMPLES_DIR = Path(__file__).parent.joinpath("data")
SAMPLES_1 = [SAMPLES_DIR.joinpath(f"sample-1/take-{i}.log") for i in range(1, 4)]
SAMPLES_2 = [SAMPLES_DIR.joinpath(f"sample-2/take-{i}.log") for i in range(1, 5)]


def fpcalc_mock(filepath, length):
    name, subpackage = filepath.parts[-1:-3:-1]
    lines = resources.read_text(f"tests.data.{subpackage}", name).splitlines()
    return [int(value) for value in lines[1].strip("FINGERPRINT=").split(",")]


def sort_sublist(pairs):
    return sorted(pair.__class__(sorted(pair)) for pair in pairs)


def test_pair_two_files():
    file1 = SAMPLES_DIR.joinpath("sample-1/take-1.log")
    file2 = SAMPLES_DIR.joinpath("sample-1/take-2.log")
    pairs = match.pair(file1, file2, patterns=["*"])
    assert sort_sublist(pairs) == [(SAMPLES_1[0], SAMPLES_1[1])]


def test_pair_files_in_directory():
    directory = SAMPLES_DIR.joinpath("sample-1")
    pairs = match.pair(directory, patterns=["*.log"])
    assert sort_sublist(pairs) == [
        (SAMPLES_1[0], SAMPLES_1[1]),
        (SAMPLES_1[0], SAMPLES_1[2]),
        (SAMPLES_1[1], SAMPLES_1[2]),
    ]


def test_pair_a_file_and_all_files_in_a_directory():
    file = SAMPLES_DIR.joinpath("sample-1/take-1.log")
    directory = SAMPLES_DIR.joinpath("sample-1")
    pairs = list(match.pair(file, directory, patterns=["*.log"]))
    assert sort_sublist(pairs) == [
        (SAMPLES_1[0], SAMPLES_1[0]),
        (SAMPLES_1[0], SAMPLES_1[1]),
        (SAMPLES_1[0], SAMPLES_1[2]),
    ]


def test_pair_directories():
    directory1 = SAMPLES_DIR.joinpath("sample-1")
    directory2 = SAMPLES_DIR.joinpath("sample-2")
    pairs = match.pair(directory1, directory2, patterns=["*.log"])
    assert sort_sublist(pairs) == [
        (sample_1, sample_2) for sample_1 in SAMPLES_1 for sample_2 in SAMPLES_2
    ]
