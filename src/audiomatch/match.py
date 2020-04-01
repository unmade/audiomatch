import concurrent.futures
import functools
import itertools
import time
from pathlib import Path
from typing import Iterator, List, Tuple

from audiomatch import fingerprints

PATTERNS = ("*.caf", "*.m4a", "*.mp3")


def match(*paths: Path, length, patterns=PATTERNS):
    pairs = list(pair(*paths, patterns=patterns))

    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        files = list(set(itertools.chain.from_iterable(pairs)))
        func = functools.partial(fingerprints.calc, length=length)
        fps = {files[i]: fp for i, fp in enumerate(executor.map(func, files)) if fp}
    print(f"fpcalc elapsed in: {time.time() - start}")

    start = time.time()
    scores = [fingerprints.compare(fps[a], fps[b]) for a, b in pairs]
    print(f"elapsed: {time.time() - start}")

    return dict(zip(pairs, scores))


def pair(*paths: Path, patterns: List[str]) -> Iterator[Tuple[Path, Path]]:
    files = []
    for path in paths:
        if path.is_dir():
            for pattern in patterns:
                files.append([p for p in path.glob(pattern)])
        else:
            files.append([path])

    if len(paths) == 1 and paths[0].is_dir():
        return itertools.combinations(*files, 2)
    elif len(paths) > 1:
        return itertools.chain.from_iterable(
            itertools.product(*group) for group in itertools.combinations(files, 2)
        )
    else:
        raise ValueError
