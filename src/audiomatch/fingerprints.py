from __future__ import annotations

import statistics
import subprocess
from pathlib import Path
from typing import Iterator, List, Tuple, Union

from audiomatch import popcount

CONFIDENCE_SCORE = 0.665
CORRECTION = 0.95
SCORE_MEDIAN_DELTA = 0.04


def calc(path: Path, length: int = 120) -> List[int]:
    # TODO: Probably it would be better to parse json output
    fp = subprocess.run(
        ["fpcalc", "-rate", "11025", "-raw", "-length", str(length), str(path)],
        stdout=subprocess.PIPE,
    )
    if lines := fp.stdout.decode().splitlines():
        return [int(value) for value in lines[1].strip("FINGERPRINT=").split(",")]
    return []


def compare(fp1: List[int], fp2: List[int]) -> float:
    # Take first 30 seconds of the the shortest fingerprint and try to find it in a
    # longer one
    if len(fp1) > len(fp2):
        return find_best_score(fp1, fp2[: seconds(30)])
    else:
        return find_best_score(fp2, fp1[: seconds(30)])


def find_best_score(fp1: List[int], fp2: List[int]) -> float:
    # Fingerprints lesser than 10 seconds don't have enough data for analysis
    if len(fp1) > seconds(10) and len(fp2) > seconds(10):
        results = [correlation(_fp1, _fp2) for _fp1, _fp2 in cross(fp1, fp2)]
        score = max(results)

        # With this score we assume two fingerprints are similar
        if score >= CONFIDENCE_SCORE:
            return score

        i = results.index(score)

        # A lot of false positives happen with fingerprints less than 20 sec, so we need
        # to slightly correct the score. If it really matches another fingerprint the
        # score will be high enough to not be affected by this
        if min(len(fp1), len(fp2)) < seconds(20):
            score *= CORRECTION

        # Usually, when two fingerprints match they have a high score at a match point
        # and lesser scores before and after match point. This assumption helps us
        # avoid false positives - they tend to have rather the same score regardless
        # of how fingerprints are aligned
        offset = 5
        samples = results[i - offset : i] + results[i + 1 : i + offset + 1]
        if score - statistics.median(samples) > SCORE_MEDIAN_DELTA:
            return score

    return 0.0


def correlation(fp1: List[int], fp2: List[int]) -> float:
    error = sum(popcount.popcount(x ^ y) for x, y in zip(fp1, fp2))
    return 1.0 - error / 32.0 / min(len(fp1), len(fp2))


def cross(fp1: List[int], fp2: List[int]) -> Iterator[Tuple[List[int], List[int]]]:
    length = min(len(fp1), len(fp2))
    span = min(length // 4, seconds(5))
    limit = max(len(fp1), len(fp2)) - length - span
    step = seconds(0.3)
    # No need to trim the second fingerprint, as 'zip' will trim it automatically
    for offset in range(span, 0, -step):
        yield fp2[offset:], fp1
    for offset in range(0, limit, step):
        yield fp1[offset:], fp2


def seconds(x: Union[int, float]) -> int:
    return round(x * 7)
