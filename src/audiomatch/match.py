import concurrent.futures
import functools
import itertools
import operator
import pathlib
import time

from audiomatch import fingerprints

EXTENSIONS = ["mp3", "m4a", "caf"]


def match(path, length):
    start = time.time()

    files = list(
        itertools.chain.from_iterable(
            (pathlib.Path(path).glob(f"*.{extension}") for extension in EXTENSIONS)
        )
    )
    with concurrent.futures.ThreadPoolExecutor() as executor:
        func = functools.partial(fingerprints.calc, length=length)
        fps = {
            files[i].name: fp for i, fp in enumerate(executor.map(func, files)) if fp
        }
    print(f"fpcalc elapsed in: {time.time() - start}")

    start = time.time()
    pairs = itertools.combinations(fps.values(), 2)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        scores = executor.map(fingerprints.compare, pairs)
    print(f"elapsed: {time.time() - start}")

    names = itertools.combinations(fps.keys(), 2)
    results = sorted(zip(names, scores), key=operator.itemgetter(0))
    for (name1, name2), score in results:
        if 0.61 <= score <= 1:
            print(f"{name1:34.34} : {name2:34.34} = {score:.3f}")
