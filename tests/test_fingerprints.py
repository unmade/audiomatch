from importlib import resources
from subprocess import CompletedProcess
from typing import List
from unittest import mock

import pytest

from audiomatch import fingerprints


def _load_fp(filepath: str) -> List[int]:
    subpackage, name = filepath.split("/")
    lines = resources.read_text(f"tests.data.{subpackage}", name).splitlines()
    return [int(value) for value in lines[1].strip("FINGERPRINT=").split(",")]


def test_calc():
    fp = resources.read_binary("tests.data.sample_1", "take-1.log")
    fpcalc = mock.MagicMock(spec=CompletedProcess, stdout=fp)
    with mock.patch("subprocess.run", return_value=fpcalc) as fpcalc_mock:
        fp = fingerprints.calc("/path/to/audio", length=120)
    assert fp == _load_fp("sample_1/take-1.log")
    assert fpcalc_mock.called


def test_calc_empty_fingerprint():
    fp = b""
    fpcalc = mock.MagicMock(spec=CompletedProcess, stdout=fp)
    with mock.patch("subprocess.run", return_value=fpcalc) as fpcalc_mock:
        fp = fingerprints.calc("/path/to/audio", length=120)
    assert fp == []
    assert fpcalc_mock.called


@pytest.mark.parametrize(
    ["a", "b", "score"],
    [
        ("sample_1/take-1.log", "sample_1/take-1.log", 1.00),
        ("sample_1/take-1.log", "sample_1/take-2.log", 0.77),
        ("sample_1/take-1.log", "sample_2/take-2.log", 0.00),
        ("sample_1/take-3.log", "sample_2/take-4.log", 0.00),
        ("sample_2/take-1.log", "sample_2/take-2.log", 0.66),
        ("sample_2/take-4.log", "sample_2/take-1.log", 0.63),
    ],
)
def test_compare(a, b, score):
    fp1 = _load_fp(a)
    fp2 = _load_fp(b)
    assert round(fingerprints.compare(fp1, fp2), 2) == score


def test_compare_add_correction_for_short_fingerprints():
    fp1 = _load_fp("edgecase_1/sample-1.log")
    fp2 = _load_fp("edgecase_1/sample-2.log")
    assert fingerprints.compare(fp1, fp2) == 0.0


def test_compare_returns_immediately_for_score_greater_than_confidence_score():
    fp1 = _load_fp("edgecase_2/sample-1.log")
    fp2 = _load_fp("edgecase_2/sample-2.log")
    assert fingerprints.compare(fp1, fp2) > fingerprints.CONFIDENCE_SCORE


def test_compare_requires_fingerprints_to_be_at_least_10_seconds_long():
    fp1 = _load_fp("edgecase_3/sample-1.log")
    fp2 = _load_fp("edgecase_3/sample-2.log")
    assert fingerprints.compare(fp1, fp2) == 0.0


def test_compare_false_positive():
    # This two completely different fingerprints initially have a relatively good score.
    # 'compare' handles these cases by checking difference between median and max value.
    fp1 = _load_fp("edgecase_4/sample-1.log")
    fp2 = _load_fp("edgecase_4/sample-2.log")
    assert fingerprints.compare(fp1, fp2) == 0.0
