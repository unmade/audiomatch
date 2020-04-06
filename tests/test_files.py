from pathlib import Path

import pytest

from audiomatch import files
from audiomatch.exceptions import NotEnoughFiles

SAMPLES_DIR = Path(__file__).parent.joinpath("data")
SAMPLES_1 = [SAMPLES_DIR.joinpath(f"sample_1/take-{i}.log") for i in range(1, 4)]
SAMPLES_2 = [SAMPLES_DIR.joinpath(f"sample_2/take-{i}.log") for i in range(1, 5)]


def sort_sublist(pairs):
    return sorted(pair.__class__(sorted(pair)) for pair in pairs)


def test_pair_two_files():
    file1 = SAMPLES_DIR.joinpath("sample_1/take-1.log")
    file2 = SAMPLES_DIR.joinpath("sample_1/take-2.log")
    pairs = files.pair(file1, file2)
    assert sort_sublist(pairs) == [(SAMPLES_1[0], SAMPLES_1[1])]


def test_pair_files_in_a_directory():
    directory = SAMPLES_DIR.joinpath("sample_1")
    pairs = files.pair(directory, extensions=[".log"])
    assert sort_sublist(pairs) == [
        (SAMPLES_1[0], SAMPLES_1[1]),
        (SAMPLES_1[0], SAMPLES_1[2]),
        (SAMPLES_1[1], SAMPLES_1[2]),
    ]


def test_pair_a_file_and_all_files_in_a_directory():
    file = SAMPLES_DIR.joinpath("sample_1/take-1.log")
    directory = SAMPLES_DIR.joinpath("sample_1")
    pairs = files.pair(file, directory, extensions=[".log"])
    assert sort_sublist(pairs) == [
        (SAMPLES_1[0], SAMPLES_1[0]),
        (SAMPLES_1[0], SAMPLES_1[1]),
        (SAMPLES_1[0], SAMPLES_1[2]),
    ]


def test_pair_directories():
    directory1 = SAMPLES_DIR.joinpath("sample_1")
    directory2 = SAMPLES_DIR.joinpath("sample_2")
    pairs = files.pair(directory1, directory2, extensions=[".log"])
    assert sort_sublist(pairs) == [
        (sample_1, sample_2) for sample_1 in SAMPLES_1 for sample_2 in SAMPLES_2
    ]


def test_pair_glob():
    wildcard = SAMPLES_DIR.joinpath("sample_1/*.log")
    pairs = files.pair(wildcard)
    assert sort_sublist(pairs) == [
        (SAMPLES_1[0], SAMPLES_1[1]),
        (SAMPLES_1[0], SAMPLES_1[2]),
        (SAMPLES_1[1], SAMPLES_1[2]),
    ]


def test_pair_one_file():
    file = SAMPLES_DIR.joinpath("sample_1/take-1.log")
    with pytest.raises(NotEnoughFiles) as excinfo:
        files.pair(file)
    assert str(excinfo.value) == "Not enough input files."
