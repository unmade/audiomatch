from __future__ import annotations

import glob
import itertools
from pathlib import Path
from typing import Iterable, Iterator, Optional, Tuple

from audiomatch.constants import DEFAULT_EXTENSIONS
from audiomatch.exceptions import NotEnoughFiles


def pair(
    *paths: Path, extensions: Optional[Iterable[str]] = None
) -> Iterator[Tuple[Path, Path]]:
    """
    Returns a cartesian product of all files found in paths.

    Args:
        *paths: a filepath, glob-style pattern or a directory.
        extensions: only take files with given extensions. It has no effect for paths
        that already have extension.

    Raises:
        ValueError: If only single file found in paths.

    Returns: A 2-length tuples where each element is a filepath.
    """
    if extensions is None:
        extensions = DEFAULT_EXTENSIONS

    files = []
    for path in paths:
        if path.is_dir():
            path = path.joinpath("*")
        files.append(
            [
                Path(pathname)
                for pathname in glob.iglob(str(path))
                if path.suffix or Path(pathname).suffix in extensions
            ]
        )

    if len(files) == 1 and len(files[0]) > 1:
        return itertools.combinations(*files, 2)
    elif len(files) > 1:
        return itertools.chain.from_iterable(
            itertools.product(*group) for group in itertools.combinations(files, 2)
        )
    else:
        raise NotEnoughFiles("Not enough input files.")
