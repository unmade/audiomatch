import operator
from importlib import resources
from pathlib import Path
from unittest import mock

import pytest

from audiomatch import match

SAMPLES_DIR = Path(__file__).parent.joinpath("data")


def sort_keys(matches):
    d = {k.__class__(sorted(k)): v for k, v in matches.items()}
    return dict(sorted(d.items(), key=operator.itemgetter(0)))


def fpcalc(filepath: Path, length):
    name, subpackage = filepath.parts[-1:-3:-1]
    package = "tests.data" if subpackage == "data" else f"tests.data.{subpackage}"
    if lines := resources.read_text(package, name).splitlines():
        return [int(value) for value in lines[1].strip("FINGERPRINT=").split(",")]
    return []


@pytest.mark.slow
def test_match():
    sample_1 = SAMPLES_DIR.joinpath("sample_1/take-1.log")
    sample_2 = SAMPLES_DIR.joinpath("sample_2/take-1.log")
    with mock.patch("audiomatch.fingerprints.calc", side_effect=fpcalc) as fpcalc_mock:
        matches = match.match(sample_1, sample_2, extensions=[".log"])
    assert sort_keys(matches) == {(sample_1, sample_2): 0.0}
    assert fpcalc_mock.call_count == 2


@pytest.mark.slow
def test_match_with_empty_fingerprint():
    sample_1 = SAMPLES_DIR.joinpath("sample_1/take-1.log")
    empty = SAMPLES_DIR.joinpath("empty.log")
    with mock.patch("audiomatch.fingerprints.calc", side_effect=fpcalc) as fpcalc_mock:
        matches = match.match(sample_1, empty, extensions=[".log"])
    assert sort_keys(matches) == {(empty, sample_1): 0.0}
    assert fpcalc_mock.call_count == 2
