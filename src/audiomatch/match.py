import concurrent.futures
import functools
import glob
import itertools
import time
from pathlib import Path
from typing import Iterator, List, Tuple

from audiomatch import fingerprints
from audiomatch.constants import DEFAULT_EXTENSIONS, DEFAULT_LENGTH


def match(*paths: Path, length=DEFAULT_LENGTH, extensions=DEFAULT_EXTENSIONS):
    pairs = list(pair(*paths, extensions=extensions))

    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        files = list(set(itertools.chain.from_iterable(pairs)))
        func = functools.partial(fingerprints.calc, length=length)
        fps = {files[i]: fp for i, fp in enumerate(executor.map(func, files)) if fp}
    print(f"fpcalc elapsed in: {time.time() - start}")

    start = time.time()
    scores = [fingerprints.compare(fps[a], fps[b]) for a, b in pairs]
    print(f"elapsed: {time.time() - start}")
    results = dict(zip(pairs, scores))
    print(results)
    return results


def pair(*paths: Path, extensions: List[str]) -> Iterator[Tuple[Path, Path]]:
    """
    Returns a cartesian product of all files found in paths.

    Args:
        *paths: a file, glob-style pattern or a directory.
        extensions: only take files with given extensions.

    Raises:
        ValueError: If only single found in paths.

    Returns: A 2-length tuples where each element is a filepath.
    """
    files = []
    for path in paths:
        if path.is_dir():
            path = path.joinpath("*")
        files.append(
            [p for s in glob.iglob(str(path)) if (p := Path(s)).suffix in extensions]
        )

    if len(files) == 1 and len(files[0]) > 1:
        return itertools.combinations(*files, 2)
    elif len(files) > 1:
        return itertools.chain.from_iterable(
            itertools.product(*group) for group in itertools.combinations(files, 2)
        )
    else:
        raise ValueError("Too few files to compare")
