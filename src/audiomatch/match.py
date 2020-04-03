from __future__ import annotations

import concurrent.futures
import functools
import itertools
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, Optional

from audiomatch import files, fingerprints
from audiomatch.constants import DEFAULT_LENGTH


def match(
    *paths: Path,
    length: int = DEFAULT_LENGTH,
    extensions: Optional[Iterable[str]] = None,
) -> Dict[FrozenSet[Path], float]:
    """
    Finds similar audio files in paths.

    Args:
        length: specifies how many seconds of the input audio to take for analysis.
            Defaults to 120.
        extensions: Take only files with given extensions. It has no effect on paths
            that already have extension.

    Returns:
        A dictionary where key is a pair of filepaths and value is a score between them.
    """
    pairs = [frozenset(pair) for pair in files.pair(*paths, extensions=extensions)]

    filepaths = list(set(itertools.chain.from_iterable(pairs)))
    func = functools.partial(fingerprints.calc, length=length)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        fps = {
            filepaths[i]: fp for i, fp in enumerate(executor.map(func, filepaths)) if fp
        }

    # Using multiprocessing.Pool.starmap method we can avoid writing wrapper to unpack
    # arguments. However, multiprocessing.Pool doesn't play nicely with coverage, and
    # require to explicitly call 'pool.join'
    with concurrent.futures.ProcessPoolExecutor() as executor:
        scores = executor.map(_compare, ((fps[a], fps[b]) for a, b in pairs))

    return dict(zip(pairs, scores))


def _compare(pair):
    """Just a wrapper for fingerprints.compare, that unpack its first argument"""
    return fingerprints.compare(*pair)
