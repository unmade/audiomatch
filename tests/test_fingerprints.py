from importlib import resources
from typing import List

import pytest

from audiomatch import fingerprints


def _load_fp(name: str) -> List[int]:
    lines = resources.read_text("tests.data", name).splitlines()
    return [int(value) for value in lines[1].strip("FINGERPRINT=").split(",")]


@pytest.mark.parametrize(["a", "b", "score"], [
    ("sample-1-take-1.log", "sample-1-take-1.log", 1.00),
    ("sample-1-take-1.log", "sample-1-take-2.log", 0.77),
    ("sample-1-take-1.log", "sample-2-take-2.log", 0.00),
    ("sample-1-take-3.log", "sample-2-take-4.log", 0.00),
    ("sample-2-take-1.log", "sample-2-take-2.log", 0.66),
    ("sample-2-take-4.log", "sample-2-take-1.log", 0.63),
])
def test_compare(a, b, score):
    fp1 = _load_fp(a)
    fp2 = _load_fp(b)
    assert round(fingerprints.compare((fp1, fp2)), 2) == score
