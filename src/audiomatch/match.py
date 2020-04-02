import concurrent.futures
import functools
import itertools
import time
from pathlib import Path

from audiomatch import files, fingerprints
from audiomatch.constants import DEFAULT_LENGTH


def match(*paths: Path, length=DEFAULT_LENGTH, extensions=None):
    pairs = list(files.pair(*paths, extensions=extensions))

    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        filepaths = list(set(itertools.chain.from_iterable(pairs)))
        func = functools.partial(fingerprints.calc, length=length)
        fps = {files[i]: fp for i, fp in enumerate(executor.map(func, filepaths)) if fp}
    print(f"fpcalc elapsed in: {time.time() - start}")

    start = time.time()
    scores = [fingerprints.compare(fps[a], fps[b]) for a, b in pairs]
    print(f"elapsed: {time.time() - start}")
    results = dict(zip(pairs, scores))
    print(results)
    return results
