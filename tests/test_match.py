from importlib import resources
from pathlib import Path
from unittest import mock

import pytest

from audiomatch import match

SAMPLES_DIR = Path(__file__).parent.joinpath("data")


def fpcalc(filepath: Path, length):
    name, subpackage = filepath.parts[-1:-3:-1]
    lines = resources.read_text(f"tests.data.{subpackage}", name).splitlines()
    return [int(value) for value in lines[1].strip("FINGERPRINT=").split(",")]


@pytest.mark.slow
def test_match():
    sample_1 = SAMPLES_DIR.joinpath("sample-1/take-1.log")
    sample_2 = SAMPLES_DIR.joinpath("sample-2/take-1.log")
    with mock.patch("audiomatch.fingerprints.calc", side_effect=fpcalc) as fpcalc_mock:
        matches = match.match(sample_1, sample_2, extensions=[".log"])
    assert matches == {frozenset((sample_1, sample_2)): 0.0}
    assert fpcalc_mock.call_count == 2
